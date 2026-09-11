# EcoData – Sistema de Alerta Temprana de Calidad del Aire (Juliaca)

**Proyecto Sello – Unidad 1 · Big Data**  
**Arquitectura:** Lambda (Batch)  
**Equipo:** EcoData

| Integrante | Dimensión U1 |
|------------|--------------|
| **Alahin Reyme Ticona Veliz** | Predicción de temperatura a partir de variables climáticas |
| **Vargas Marichi Lanzeloth** | Análisis y predicción de calidad del aire (PM2.5 / PM10) orientado a alertas |

---

## 1. Pregunta central de negocio

¿Cómo anticipar condiciones de riesgo ambiental en Juliaca combinando datos climáticos y de calidad del aire mediante un pipeline batch distribuido que permita entrenar modelos predictivos y, en una segunda etapa, emitir alertas tempranas?

## 2. Arquitectura seleccionada

Se adoptó la **arquitectura Lambda** porque el caso de negocio requiere simultáneamente:

- **Capa Batch:** análisis histórico y entrenamiento de modelos.
- **Capa Speed (Unidad 2):** alertas en tiempo casi real.

Ambas capas se alimentan de la misma fuente (Open-Meteo). La Unidad 1 implementa exclusivamente la ruta Batch.

## 3. Pipeline implementado (Unidad 1)
Open-Meteo (CSV)
→ Limpieza + controles de calidad (Silver)
→ Parquet particionado por año/mes (Gold)
→ Spark MLlib (regresión comparada)
→ Modelo ganador guardado


## 4. Resultados principales

### Dimensión Clima (Alahin Reyme Ticona Veliz)

| Elemento                        | Resultado                          |
|--------------------------------|------------------------------------|
| Registros clima (Gold)         | 26 304                             |
| Nulos / Duplicados             | 0 / 0                              |
| Particionamiento               | año + mes                          |
| PartitionFilters               | Verificado                         |
| **Mejor modelo**               | **RandomForestRegressor**          |
| **RMSE**                       | **1.4351**                         |
| **R²**                         | **0.9180**                         |
| **MAE**                        | **1.1220**                         |
| Variable más importante        | hour (0.636)                       |

### Dimensión Calidad del Aire (Vargas Marichi Lanzeloth)

| Elemento                        | Resultado                          |
|--------------------------------|------------------------------------|
| Registros procesados           | (completar)                        |
| Mejor modelo                   | (completar)                        |
| Métricas principales           | (completar)                        |

## 5. Cómo reproducir

1. Clonar este repositorio
2. Tener Docker + `lambda26/pyspark` corriendo
3. Colocar los CSV de Open-Meteo en la ruta de datos del contenedor
4. Ejecutar los notebooks:
   - `notebooks/01_pipeline_completo_u1.ipynb` (dimensión clima)
   - Notebook de calidad del aire (dimensión aire)

## 6. Estructura del repositorio

- `notebooks/` → Pipelines reproducibles por dimensión
- `docs/` → Documentación formal (arquitectura, dimensiones, producto U1)
- `diagrams/` → Arquitectura Lambda
- `data/` → Instrucciones de los datasets
- `artifacts/` → Modelos y salidas (ignorados por tamaño)

## 7. Próximos pasos (Unidad 2)

- Incorporar streaming con Kafka
- Inferencia en tiempo real de los modelos
- Alertas tempranas de calidad del aire