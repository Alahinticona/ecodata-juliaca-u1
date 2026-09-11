# Resultados y evidencias – Unidad 1

## Calidad de datos (común)
- Schema explícito
- Nulos = 0
- Duplicados = 0
- PartitionFilters verificado

## Dimensión Clima (Alahin)
- 26 304 registros
- RandomForest: RMSE 1.4351 | R² 0.9180 | MAE 1.1220
- Modelo guardado en `/opt/ecodata/models/clima_rf_model`

## Dimensión Aire (Lanzeloth)
- (Completar con resultados reales del compañero)

## Evidencias disponibles
- Notebooks reproducibles
- Parquet particionado
- Tablas comparativas de modelos
- Gráficos de importancia de variables
- Diagrama de arquitectura Lambda