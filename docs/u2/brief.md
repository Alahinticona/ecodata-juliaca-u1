# Brief de la Unidad 2: EcoData en tiempo real

**Equipo:** EcoData · Alahin Reyme Ticona Veliz (dimensión clima) y Lanzeloth Vargas Marichi (dimensión aire)
**Curso:** Big Data 2026-2 · **Evaluación:** S12, 30/10/2026 · **Versión:** 3

## 1. Problema
En la Unidad 1 EcoData construyó la ruta **Batch** de su arquitectura Lambda: procesa el histórico de Juliaca y entrena un modelo una sola vez. Ese resultado es una foto fija; no avisa nada cuando llega un dato nuevo. La Unidad 2 construye la ruta **Speed**: cada lectura se procesa al llegar, se pronostica la hora siguiente y el error del modelo se mide en vivo.

## 2. Objetivo
Un pipeline de eventos de punta a punta, con dos dimensiones sobre la misma arquitectura:

| Dimensión | Pregunta | Línea base |
|---|---|---|
| Aire (Lanzeloth) | ¿Se pronostica el PM2.5 de la próxima hora mejor que repitiendo la última? | Persistencia |
| Clima (Alahin) | ¿Se pronostica la temperatura de la próxima hora mejor que repitiendo la última? | Persistencia y persistencia diaria |

La pregunta inicial («¿cuándo se superará el umbral?») se descartó: en 2023 el PM2.5 nunca superó la norma ECA (p95 ≈ 10,5 µg/m³), así que no había casos positivos que medir.

## 3. Alcance
**Incluye:** ingesta por Kafka, Spark Structured Streaming con ventana, watermark y checkpoint, inferencia con MLlib, eventos de negocio, observabilidad en Grafana, costos y documentación.
**No incluye:** sensores propios en producción. La fuente es Open-Meteo (dato modelado: CAMS para aire, reanálisis y pronóstico para clima). El ESP32 con HC-SR04 queda como fuente secundaria y su perfil se conserva en el código base. Está pendiente de confirmar con el docente.

## 4. Arquitectura
Open-Meteo → `atmos-aire` / `atmos-clima` → Spark (consultas de ventanas e inferencia) → Pushgateway → Prometheus → Grafana, y eventos de negocio a `atmos-negocio`.

## 5. Decisiones técnicas
- **Ventana de 6 h y watermark de 2 h:** la fuente entrega un evento por hora; 2 h tolera el retraso normal de la API.
- **Modelo:** `Pipeline(VectorAssembler + GBTRegressor)` que predice el **cambio** a una hora, con split cronológico 80/20 y una sola función de variables para entrenamiento y servicio.
- **Evento de negocio:** `aire.episodio` (PM2.5 sobre el p95 de entrenamiento) y `clima.helada` (T < 0 °C).
- **Observabilidad:** métricas con prefijos `lambda26_aire_` y `lambda26_clima_` en un tablero unificado.

## 6. Resultados medidos
| | Aire | Clima |
|---|---|---|
| MAE modelo en prueba | 0,473 | 0,537 |
| MAE persistencia en prueba | 0,687 | 1,096 |
| Mejora en prueba | −31,1 % | −51,0 % |
| MAE en vivo (modelo / persistencia) | 0,422 / 0,567 | 0,536 / 0,982 |
| Mejora en vivo | −25,5 % (761 h) | −45,5 % (757 h) |
| Descartes del watermark (demo) | 0 → 2 | 0 → 2 |

## 7. Costo de referencia
US$ 91,15 al mes con 3 × t3.medium (precios de referencia, no una factura).

## 8. Roles
| Persona | Responsabilidad |
|---|---|
| Alahin Reyme Ticona Veliz | Dimensión clima: modelo de temperatura, job `s12_streaming_clima.py`, defensa propia |
| Lanzeloth Vargas Marichi | Dimensión aire: modelo de PM2.5, job `s12_streaming_aire.py`, defensa propia |
| Ambos | Kafka, Grafana, documentación, repositorio |

## 9. Riesgos y límites
| Riesgo | Mitigación |
|---|---|
| Sin internet para la API el día de la demo | Replay desde archivo y capturas de respaldo |
| Dato modelado, un año y una ubicación | Declarado como límite; no se generaliza |
| Historia de 24 h en memoria del job | No reiniciar en la demo; pasa a una tabla en U3 |
| Sin exactly-once de punta a punta | Documentado: Kafka y `foreachBatch` son al menos una vez |

## 10. Entregables
Repositorio con topics, MkDocs publicado, scripts, tablero Grafana, pitch y guion de cada integrante, y capturas de respaldo.
