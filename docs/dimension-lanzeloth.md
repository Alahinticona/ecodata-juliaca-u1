# Dimensión U1 – Vargas Marichi Lanzeloth

## Enfoque
Análisis y predicción de **calidad del aire (PM2.5 y PM10)** en Juliaca, orientado a la identificación de niveles de riesgo y a la futura generación de alertas tempranas.

## Pregunta de esta dimensión
¿Cómo se comportan los indicadores de contaminación (PM2.5 / PM10) y qué modelos permiten anticipar episodios de alta contaminación para emitir alertas?

## Pipeline realizado
1. Extracción de datos de calidad del aire desde Open-Meteo
2. Limpieza y controles de calidad (nulos, duplicados, rangos físicos)
3. Creación de variable de nivel de riesgo (Bajo / Moderado / Alto)
4. Escritura en Parquet particionado
5. Entrenamiento de modelo de regresión o clasificación orientado a contaminación
6. Definición de umbrales de alerta

## Resultados esperados / obtenidos
| Elemento | Valor |
|----------|-------|
| Registros procesados | (completar con el número real) |
| Variable objetivo | pm2_5 / pm10 o nivel_riesgo |
| Mejor modelo | (completar) |
| Métricas principales | (completar RMSE/R² o Accuracy/F1) |
| Umbrales de alerta propuestos | PM2.5 ≥ 25 (Moderado), ≥ 50 (Alto) |

## Aporte al equipo
Esta dimensión entrega la capa de contaminación y los criterios de alerta. Junto con la dimensión climática de Alahin, forma la base completa del sistema de alerta temprana que se potenciará en la Unidad 2 con streaming.