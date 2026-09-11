# Producto Unidad 1 – EcoData (Juliaca)

**Estudiante:** [Alahin Reyme Ticona Veliz] 
**Estudiante:** [VARGAS MARICHI lanzeloth]  
**Equipo:** EcoData  
**Dimensión U1:** Influencia de variables climáticas sobre condiciones ambientales en Juliaca (enfoque predictivo)

---

## 1. Pregunta central y dimensión U1

**Pregunta de negocio del equipo:**  
¿Cómo anticipar episodios de riesgo ambiental en Juliaca combinando datos climáticos y de calidad del aire?

**Mi dimensión U1 (predictiva batch):**  
Construir un pipeline batch distribuido que limpie, valide y particione datos climáticos de Open-Meteo y entrene un modelo de regresión capaz de predecir temperatura a partir de viento, humedad y variables temporales, dejando la base lista para extenderse a predicción de PM2.5/PM10.

---

## 2. Arquitectura seleccionada

**Lambda**

Se eligió Lambda porque el proyecto necesita:
- Análisis histórico y entrenamiento de modelos (Batch)
- Alertas en tiempo casi real (Speed – Unidad 2)

La Unidad 1 implementa solo la ruta Batch.

---

## 3. Pipeline implementado

| Capa   | Contenido                                      | Tecnología      |
|--------|------------------------------------------------|-----------------|
| Bronze | CSV crudos de Open-Meteo                       | Descarga API    |
| Silver | Schema explícito, 0 nulos, 0 duplicados        | PySpark         |
| Gold   | Parquet particionado por año y mes             | partitionBy     |
| ML     | VectorAssembler + 3 LR + RandomForest + guardado | Spark MLlib   |

---

## 4. Controles de calidad aplicados (S3)

- Schema explícito
- Nulos = 0
- Duplicados = 0 (por `time`)
- Filtrado de rango físico
- Verificación de conteo ida y vuelta
- PartitionFilters confirmado en `explain(True)`

---

## 5. Componente ML (S4)

- **Objetivo:** temperature_2m
- **Predictores:** wind_speed_10m, wind_direction_10m, relative_humidity_2m, hour, mes
- **Modelos comparados:** LR sin reg, LR Ridge, LR ElasticNet, RandomForest
- **Métricas:** RMSE, R², MAE
- **Modelo guardado:** artifacts/modelo_temperatura_ganador

---

## 6. Conclusiones

Se completó el pipeline batch de la Unidad 1: datos confiables en capa Gold y primer modelo de regresión distribuida comparado y guardado.

**Siguiente paso (Unidad 2):** streaming + inferencia en tiempo real + alertas.