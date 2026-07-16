# Memoria Técnica Breve

## 1. Resumen Ejecutivo
FridgeChef AI es un asistente de cocina inteligente interactivo orientado a minimizar el desperdicio de comida en el hogar. La aplicación permite a los usuarios ingresar sus ingredientes mediante texto o cargando una imagen de su nevera, aplicando al instante restricciones alimentarias (dietas, alergias) y límites de tiempo para obtener recetas personalizadas que priorizan el aprovechamiento alimentario.

## 2. Arquitectura del Sistema
La aplicación se compone de un flujo de tres capas desacopladas:
* Presentación (Frontend): Implementada en Streamlit debido a su velocidad de prototipado y manejo ágil de estado en Python.
* Orquestación e IA (Backend): SDK oficial de google-genai conectado al modelo multimodal gemini-2.5-flash.
* Capa de Datos: Definición estricta de un contrato JSON por medio de google.genai.types.Schema para controlar la respuesta del LLM de manera estructurada.

## 3. Mitigación de Alucinaciones y Calidad de la IA
Para cumplir con los criterios de evaluación del curso, se han adoptado las siguientes medidas:
1. Baja Temperatura ($T = 0.2$): Garantiza que el modelo actúe de manera determinista y no invente ingredientes principales fuera de los provistos por el usuario.
2. Esquema de Datos Estricto (Structured Outputs): Evita la inyección de formatos inesperados que rompan la UI, forzando la salida del modelo a ajustarse exactamente a la estructura predefinida.
3. Prompt de Rol (System Prompt): Instruye explícitamente sobre la viabilidad, el control de alergias cruzadas y la obligatoriedad de que la receta base se elabore únicamente con los ingredientes disponibles.
