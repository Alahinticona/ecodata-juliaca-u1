# EcoData – Sistema de Alerta Temprana de Calidad del Aire (Juliaca)

**Proyecto Sello – Unidad 1 · Big Data**  
**Arquitectura:** Lambda (Batch)  
**Equipo:** EcoData

| Integrante | Dimensión U1 |
|------------|--------------|
| **Alahin Reyme Ticona Veliz** | Predicción de temperatura a partir de variables climáticas |
| **Vargas Marichi Lanzeloth** | Análisis y predicción de calidad del aire (PM2.5/PM10) orientado a alertas |

---

## Pregunta central del equipo

¿Cómo anticipar condiciones de riesgo ambiental en Juliaca combinando datos climáticos y de calidad del aire mediante un pipeline batch distribuido?

## Arquitectura

**Lambda**:  
- Ruta Batch (Unidad 1) → análisis histórico + modelos  
- Ruta Speed (Unidad 2) → alertas en tiempo real

## Resultados principales (Unidad 1)

### Dimensión Clima (Alahin)
| Métrica | Valor |
|---------|-------|
| Registros | 26 304 |
| Mejor modelo | RandomForest |
| RMSE | 1.4351 |
| R² | 0.9180 |
| MAE | 1.1220 |

### Dimensión Calidad del Aire (Lanzeloth)
| Métrica | Valor |
|---------|-------|
| Registros | (completar) |
| Mejor modelo | (completar) |
| Métricas | (completar) |