# Producto Unidad 1 – EcoData (Juliaca)

**Equipo:** EcoData  
**Arquitectura:** Lambda (Batch)  
**Integrantes:**  
- Alahin Reyme Ticona Veliz  
- Vargas Marichi Lanzeloth

---

## 1. Pregunta central del equipo
¿Cómo anticipar condiciones de riesgo ambiental en Juliaca combinando datos climáticos y de calidad del aire mediante un pipeline batch distribuido?

## 2. Dimensiones U1

| Integrante | Dimensión | Variable objetivo |
|------------|-----------|-------------------|
| Alahin Reyme Ticona Veliz | Predicción climática | temperature_2m |
| Vargas Marichi Lanzeloth | Calidad del aire y alertas | pm2_5 / pm10 / nivel_riesgo |

## 3. Arquitectura
**Lambda**. La Unidad 1 implementa la ruta Batch. La ruta Speed se desarrolla en Unidad 2.

## 4. Pipeline común
Open-Meteo → Limpieza + Calidad → Parquet particionado (Gold) → Spark MLlib → Modelo guardado

## 5. Resultados principales

### Dimensión Clima (Alahin)
- Registros: 26 304
- Mejor modelo: RandomForest
- RMSE: 1.4351 | R²: 0.9180 | MAE: 1.1220
- Variable más importante: hour (0.636)

### Dimensión Aire (Lanzeloth)
- Registros: (completar)
- Mejor modelo: (completar)
- Métricas: (completar)

## 6. Conclusión
Se completó el pipeline batch de la Unidad 1 con dos dimensiones complementarias. La base está lista para incorporar streaming e inferencia en tiempo real en la Unidad 2.