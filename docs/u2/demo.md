# Guion de la demo (Lanzeloth y Alahin)

Tiempos propuestos; ajústalos al que asigne el docente.

## Antes de entrar (15 min antes)
1. Doble clic en `levantar.bat`. Verifica en http://localhost:49090/targets que `pushgateway` esté UP.
2. Jupyter (http://localhost:4488) → `s12-ecodata/12_ecodata_u2.ipynb`. Ejecuta las secciones 0 a 3 y lanza los jobs (sección 6).
3. Publica datos (celdas de la sección 3) y repite cada 10 min para mantener el semáforo en verde.
4. Abre Grafana (Last 15 min, refresco 5 s), Kafka UI y Prometheus `/alerts`.

## Pitch (3 min)
| Min | Quién | Qué decir |
|---|---|---|
| 1 | Lanzeloth | Problema (aire y clima en Juliaca) y pregunta reformulada |
| 1 | Alahin | Arquitectura Lambda: ruta Speed |
| 1 | Lanzeloth | Honestidad de la fuente y del modelo |

## Demo técnica (10 min)
| Min | Quién | Acción | Criterio |
|---|---|---|---|
| 2 | Lanzeloth | Notebook 1–3: API → evento JSON → Kafka | 1, 2 |
| 1 | Lanzeloth | Notebook 4 y Kafka UI: conteo y mensajes | 1, 2 |
| 2 | Alahin | Streaming: ventanas, watermark. Publicar `--tardio` y ver descartes | 3 |
| 2 | Alahin | Prometheus: targets, alertas; semáforo en Grafana | 4 |
| 2 | Lanzeloth | Notebook 5 y Grafana: predicción +1 h y MAE vs persistencia | 6, 7 |
| 1 | Ambos | Costos y escalado ([operacion.md](operacion.md)) | 5 |

## Si te piden cambiar el rango o desconectar
- Rango corto: Grafana → selector de tiempo → *Last 5 minutes*.
- Desconectar: notebook sección 8 (cierra productor y jobs). El semáforo se pondrá rojo, y es lo esperado.

## Preguntas probables
Ver [s12-preparacion.md](s12-preparacion.md), sección 2.

## Plan B
Si falla la red: usar el replay desde archivo (`--archivo`), que no depende de la API. Si falla algo de Docker: mostrar las capturas guardadas en `docs/assets/u2/`.
