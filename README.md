# 🍳 FridgeChef AI

**FridgeChef AI** es un asistente de cocina inteligente desarrollado como proyecto para el curso de Inteligencia Artificial de Google. La aplicación ayuda a reducir el desperdicio de comida transformando ingredientes sueltos de la nevera en recetas deliciosas, viables y personalizadas en segundos.

Este sistema utiliza **Gemini 2.5 Flash** para procesar texto e imágenes, aplicando restricciones de alergias, dietas y tiempo, asegurando resultados libres de "alucinaciones" mediante salidas JSON estructuradas.

---

## 🚀 Características del MVP & Extensiones

- **Detección por Imagen (Visión AI):** Sube una foto de tu nevera y la IA identificará automáticamente los ingredientes principales.
- **Entrada Manual Flexible:** Edita o añade ingredientes de forma manual para complementar el análisis.
- **Filtros Personalizados:** Restricciones de dieta (vegetariana, vegana, keto, etc.), alergias o ingredientes excluidos, y tiempo de preparación máximo.
- **Salida Estructurada Seguro (JSON Schema):** La interfaz procesa un objeto JSON estricto enviado por Gemini para asegurar un diseño limpio y robusto.
- **Recetas Viables y Reales:** Temperatura del modelo configurada a `0.2` para evitar que la IA invente ingredientes que no tienes.
- **Consejo Anti-Desperdicio:** Cada receta incluye un tip práctico de conservación o prioridad de consumo.

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.10+
- **Frontend / UI:** [Streamlit](https://streamlit.io/)
- **Cerebro de IA:** SDK oficial de `google-genai` (Modelo: `gemini-3.5-flash`)
- **Procesamiento de Imagen:** Pillow (PIL)

---

## 📦 Instalación y Configuración Local

Sigue estos pasos para hacer funcionar el proyecto en tu máquina local:

### 1. Clonar el repositorio
```bash
git clone https://github.com/emmillan42/fridgechef-ai.git fridgechef-ai
cd fridgechef-ai
```
Dentro de esa carpeta deben estar al menos los siguientes archivos necesarios:
1. **`app.py`**: Con el código de Streamlit completo que incluye la interfaz, la conexión con Gemini y la lógica de Visión AI.
2. **`requirements.txt`**: con las librerías requeridas por la aplicación:
   ```text
   streamlit
   google-genai
   pillow
3. **`README.md`**; el archivo con la breve descripción del proyecto.

### 2. Crear y activar un entorno virtual (Recomendado)
```bash
# En Windows:
python -m venv venv
.\venv\Scripts\activate

# En macOS/Linux:
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

Crea un archivo requirements.txt con las librerías necesarias e instálalas:
```bash
pip install -r requirements.txt
```
*(Contenido de requirements.txt: streamlit, google-genai, pillow)*

### 4. Configurar tu API Key de Gemini

Para que el modelo funcione, necesitas una clave de API de Google AI Studio. Consigue tu API Key de Gemini (Si no la tienes)

1. Ve a Google AI Studio.
2. Inicia sesión con tu cuenta de Google.
3. Haz clic en "Get API key" (Obtener clave de API) y luego en "Create API key".
4. Copia esa clave (es una cadena larga de letras y números).

En Windows (CMD):
```dos
set GEMINI_API_KEY="tu_api_key_aqui"
```

En macOS/Linux o Git Bash:
```bash
export GEMINI_API_KEY="tu_api_key_aqui"
```

---

## 💻 Ejecución de la App

Una vez configurada la API Key y con el entorno virtual activo, ejecuta:
```bash
streamlit run app.py
```
Abre cualquier navegador (Chrome, Edge, Firefox, etc.) e ingresa a la dirección:
```Plaintext
Local URL: http://localhost:8501
Network URL: http://172.xx.xx.xx:8501
```
¡Ahí verás la app de FridgeChef AI completamente funcional en directo!
