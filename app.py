import streamlit as st
import json
from PIL import Image
from google import genai
from google.genai import types
# Nueva importación para manejar la cuenta de servicio de Google Cloud
from google.oauth2 import service_account

# 1. Configuración de la página de Streamlit
st.set_page_config(page_title="FridgeChef AI", page_icon="🍳", layout="centered")
st.title("🍳 FridgeChef AI")
st.write("¡Transforma tu nevera en deliciosas recetas y reduce el desperdicio!")

# --- INICIALIZACIÓN DEL ESTADO DE SESIÓN (Persistencia de datos) ---
if "ingredientes_text" not in st.session_state:
    st.session_state["ingredientes_text"] = ""
if "resultado_recetas" not in st.session_state:
    st.session_state["resultado_recetas"] = None

# 2. Inicialización del cliente de Gemini con Autodetect y Fallback
@st.cache_resource
def get_gemini_client():
    # --- PASO 1: Comprobar e intentar Cuenta de Servicio (Prioridad 1) ---
    if "gcp_service_account" in st.secrets:
        try:
            info = dict(st.secrets["gcp_service_account"])
            credentials = service_account.Credentials.from_service_account_info(info)

            project_id = st.secrets.get("gcp_project_id", info.get("project_id"))
            location = st.secrets.get("gcp_location", "us-central1")

            # Inicializamos cliente apuntando a Vertex AI
            client = genai.Client(
                vertexai=True,
                project=project_id,
                location=location,
                credentials=credentials
            )
            # Log de éxito en la consola de la terminal
            print("INFO: Autenticado con éxito usando Google Cloud Service Account (Vertex AI).")
            return client
        except Exception as e:
            # Si falla la Service Account por permisos, formato, etc., imprimimos el error en consola
            print(f"WARNING: Falló la autenticación por Service Account: {e}. Intentando fallback a API Key...")

    # --- PASO 2: Comprobar e intentar API Key desde Secrets de Streamlit (Prioridad 2) ---
    if "GEMINI_API_KEY" in st.secrets:
        print("INFO: Autenticado con éxito usando GEMINI_API_KEY desde Streamlit Secrets.")
        return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

    # --- PASO 3: Intentar API Key desde variable de entorno local (WSL/Ubuntu) ---
    import os
    if "GEMINI_API_KEY" in os.environ:
        print("INFO: Autenticado con éxito usando GEMINI_API_KEY desde variables de entorno locales.")
        return genai.Client()

    # --- PASO 4: Error si no encuentra absolutamente nada ---
    raise ValueError(
        "No se detectaron credenciales válidas. Configura 'gcp_service_account' o 'GEMINI_API_KEY' "
        "en tus secrets de Streamlit o variables de entorno."
    )

try:
    client = get_gemini_client()
except Exception as e:
    st.error(f"Error crítico de autenticación: {e}")
    st.stop()

    # --- PASO 3: Intentar API Key desde variable de entorno local (WSL/Ubuntu) ---
    import os
    if "GEMINI_API_KEY" in os.environ:
        print("INFO: Autenticado con éxito usando GEMINI_API_KEY desde variables de entorno locales.")
        return genai.Client()

    # --- PASO 4: Error si no encuentra absolutamente nada ---
    raise ValueError(
        "No se detectaron credenciales válidas. Configura 'gcp_service_account' o 'GEMINI_API_KEY' "
        "en tus secrets de Streamlit o variables de entorno."
    )

try:
    client = get_gemini_client()
except Exception as e:
    st.error(f"Error crítico de autenticación: {e}")
    st.stop()

# 3. Extensión: Visión AI para escanear la nevera
st.subheader("📸 Escanea tu Nevera con Visión AI")
foto_nevera = st.file_uploader("Sube una foto de tu nevera o despensa", type=["jpg", "jpeg", "png"])

if foto_nevera is not None:
    try:
        imagen = Image.open(foto_nevera)
        st.image(imagen, caption="Tu nevera subida con éxito", use_container_width=True)

        if st.button("🔍 Detectar ingredientes con IA"):
            with st.spinner("Analizando la imagen..."):
                prompt_vision = """
                Analiza detalladamente esta imagen de una nevera o despensa.
                Identifica todos los ingredientes, alimentos, frutas, verduras, carnes o lácteos que sean claramente visibles.
                Devuelve únicamente una lista de los ingredientes detectados separados por comas, sin introducciones ni textos adicionales.
                Ejemplo de salida: tomate, queso, leche, pollo, lechuga
                """
                response_vision = client.models.generate_content(
                    model='gemini-3.1-flash-lite',
                    contents=[imagen, prompt_vision]
                )
                # Guardamos directamente en el estado de sesión del widget de texto
                st.session_state["ingredientes_text"] = response_vision.text.strip()
                st.success("¡Ingredientes detectados con éxito!")
    except Exception as e:
        st.error(f"Error al procesar la imagen: {e}")

# 4. Interfaz de Usuario (UI) - Captura de datos
st.sidebar.header("⚙️ Filtros y Preferencias")
dieta = st.sidebar.selectbox("Tipo de dieta", ["Ninguna", "Vegetariana", "Vegana", "Keto", "Sin Gluten"])
alergias = st.sidebar.text_input("Alergias o exclusiones (ej. maní, lactosa)", "")
tiempo_max = st.sidebar.slider("Tiempo máximo de preparación (minutos)", 10, 120, 30)

# BOTÓN DE RESET / LIMPIAR TODO
st.sidebar.markdown("---")
if st.sidebar.button("🧹 Limpiar Cocina (Empezar de nuevo)", use_container_width=True):
    st.session_state["ingredientes_text"] = ""
    st.session_state["resultado_recetas"] = None
    st.rerun()

st.subheader("📋 ¿Qué tienes en la nevera?")
# Vinculamos la caja de texto directamente al Session State mediante la propiedad 'key'
ingredientes_input = st.text_area(
    "Ingredientes disponibles (puedes editarlos o añadir más):",
    key="ingredientes_text",
    placeholder="huevos, arroz, tomate, calabacín, cebolla"
)

# 5. Definición del esquema JSON de salida
esquema_recetas = types.Schema(
    type=types.Type.OBJECT,
    properties={
        "recetas": types.Schema(
            type=types.Type.ARRAY,
            items=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "nombre": types.Schema(type=types.Type.STRING),
                    "tiempo_min": types.Schema(type=types.Type.INTEGER),
                    "ingredientes_usados": types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING)),
                    "faltantes_opcionales": types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING)),
                    "pasos": types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING)),
                    "consejo_antidesperdicio": types.Schema(type=types.Type.STRING)
                },
                required=["nombre", "tiempo_min", "ingredientes_usados", "faltantes_opcionales", "pasos", "consejo_antidesperdicio"]
            )
        )
    },
    required=["recetas"]
)

# 6. Botón de acción para generar recetas (Solo realiza la llamada a la API)
if st.button("Buscar Recetas 🚀", use_container_width=True):
    if not ingredientes_input.strip():
        st.warning("Por favor, introduce o detecta al menos un ingrediente.")
    else:
        with st.spinner("Pensando en las mejores recetas para ti... 🧑‍🍳"):
            prompt_base = f"""
            Eres un asistente experto en cocina práctica (FridgeChef AI).
            Con los siguientes ingredientes disponibles: {ingredientes_input}.

            Restricciones a respetar estrictamente:
            - Dieta: {dieta}
            - Alergias/Exclusiones: {alergias if alergias else 'Ninguna'}
            - Tiempo máximo: {tiempo_max} minutos.

            Genera exactamente 3 recetas viables y realistas.
            Regla de oro: No inventes ingredientes principales que el usuario no tiene; se permite incluir condimentos básicos (sal, aceite, pimienta) o sugerir de forma muy clara "ingredientes faltantes opcionales" que mejorarían el plato, pero el plato debe poder realizarse con lo que hay.
            Para cada receta, incluye un consejo creativo anti-desperdicio que priorice alimentos propensos a dañarse pronto.
            """

            try:
                response = client.models.generate_content(
                    model='gemini-3.1-flash-lite',
                    contents=prompt_base,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=esquema_recetas,
                        temperature=0.2
                    ),
                )

                # Guardamos el resultado en la sesión persistente en lugar de una variable local
                st.session_state["resultado_recetas"] = json.loads(response.text)

            except Exception as e:
                st.error(f"Ocurrió un error al procesar tu solicitud: {e}")

# 7. Renderizado de los resultados (Independiente del botón, persistente al 'rerun')
if st.session_state["resultado_recetas"] is not None:
    resultado = st.session_state["resultado_recetas"]
    st.success("¡Aquí tienes tus opciones personalizadas!")

    # Bloque de descarga y visualización de JSON
    json_string = json.dumps(resultado, indent=2, ensure_ascii=False)

    col_download, col_empty = st.columns([1, 2])
    with col_download:
        st.download_button(
            label="📥 Descargar JSON",
            data=json_string,
            file_name="recetas_fridgechef.json",
            mime="application/json",
            use_container_width=True
        )

    with st.expander("👾 Ver JSON de salida (Código fuente)"):
        st.json(resultado)

    # Dibujar las recetas en la pantalla
    for idx, receta in enumerate(resultado["recetas"]):
        with st.expander(f"🍽️ {receta['nombre']} — ⏱️ {receta['tiempo_min']} mins", expanded=True if idx == 0 else False):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Ingredientes que usarás:**")
                for ing in receta["ingredientes_usados"]:
                    st.write(f"- {ing}")
            with col2:
                if receta["faltantes_opcionales"]:
                    st.write("**Faltantes recomendados:**")
                    for falt in receta["faltantes_opcionales"]:
                        st.write(f"- 🛒 {falt}")
                else:
                    st.write("**¡Tienes todo lo necesario! 🎉**")

            st.write("**Pasos de preparación:**")
            for i, paso in enumerate(receta["pasos"], 1):
                st.write(f"{i}. {paso}")

            st.info(f"💡 **Consejo Anti-Desperdicio:** {receta['consejo_antidesperdicio']}")
