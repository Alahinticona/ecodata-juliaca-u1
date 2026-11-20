# Matriz de Trazabilidad

| Integrante | Dimensión | Indicador U1 (Batch) | Indicador U2 (Streaming) | Fuente y Técnica | Evidencia |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Alahin** | Predictiva (PM2.5) | Concentración histórica mensual (µg/m³) | Predicción de picos en próximas horas | Open-Meteo / Regresión (Spark MLlib) | `notebooks/01_pipeline_completo_u1.ipynb` |
| **Alahin** | Predictiva (Clima) | Influencia histórica de temp/viento | Predicción de condiciones climáticas en vivo | Open-Meteo / Clasificación (Spark MLlib) | `notebooks/S13_integracion_dataops.ipynb` |