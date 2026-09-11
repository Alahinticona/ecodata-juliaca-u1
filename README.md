# EcoData – Sistema de Alerta Temprana de Calidad del Aire (Juliaca)

**Proyecto Sello – Unidad 1 · Big Data**  
**Arquitectura:** Lambda (Batch)  
**Estudiante:** [Alahin Reyme Ticona Veliz]  
**Estudiante:** [VARGAS MARICHI lanzeloth] 
**Equipo:** EcoData

---

## 1. Pregunta central de negocio

¿Cómo anticipar condiciones climáticas y de calidad del aire en Juliaca mediante un pipeline batch distribuido que permita entrenar modelos predictivos y, en una segunda etapa, emitir alertas tempranas?

## 2. Arquitectura seleccionada

Se adoptó la **arquitectura Lambda** porque el caso de negocio requiere simultáneamente:

- **Capa Batch:** análisis histórico y entrenamiento de modelos.
- **Capa Speed (Unidad 2):** alertas en tiempo casi real.

## 3. Pipeline implementado (Unidad 1)

Open-Meteo (CSV)
→ Limpieza + controles de calidad (Silver)
→ Parquet particionado por año/mes (Gold)
→ Spark MLlib (regresión comparada)
→ Modelo ganador guardado
text


## 4. Resultados principales

| Elemento                        | Resultado      |
|--------------------------------|----------------|
| Registros clima (Gold)         | 26 304         |
| Nulos / Duplicados             | 0 / 0          |
| Particionamiento               | año + mes      |
| PartitionFilters               | Verificado     |
| Mejor modelo                   | (completar)    |
| RMSE / R² / MAE                | (completar)    |

## 5. Cómo reproducir

1. Clonar este repositorio
2. Tener Docker + `lambda26/pyspark` corriendo
3. Colocar los CSV de Open-Meteo en la ruta de datos del contenedor
4. Ejecutar el notebook: `notebooks/01_pipeline_completo_u1.ipynb`

## 6. Estructura del repositorio

- `notebooks/` → Pipeline completo reproducible
- `docs/u1-producto.md` → Documentación formal de la dimensión U1
- `diagrams/` → Arquitectura Lambda
- `data/` → Instrucciones de los datasets
- `artifacts/` → Modelos y salidas (ignorados por tamaño)