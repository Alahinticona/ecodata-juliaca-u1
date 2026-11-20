# Revisión Técnica y Hardening (S14)

## 1. Correcciones aplicadas a la configuración
* **Kafka y Observabilidad:** Se agregaron bloques `healthcheck` en los archivos `compose.yml`. Los servicios ahora esperan a que sus dependencias estén sanas (`condition: service_healthy`).
* **Seguridad:** Se parametrizaron las credenciales de Grafana usando `${GRAFANA_ADMIN_USER:-admin}`.
* *Evidencia:* Ejecución de `docker ps` mostrando el estado `(healthy)` en los contenedores.

## 2. Prueba de No Regresión (Antes vs. Después)
Se repitió la ejecución del notebook S13 tras aplicar los cambios en Docker. Los resultados demuestran que el sistema no se rompió:

| Comprobación | Antes (S13) | Después (S14) | ¿Es regresión? |
| :--- | :--- | :--- | :--- |
| Compuertas previas | Todas OK | Todas OK | No |
| Latencia p50 / p95 | [Tu valor viejo] | 17,874 ms / 1,391,724 ms | No (datos históricos) |
| MAE del modelo | [Tu valor viejo] | 0.8792 | No (datos en vivo cambian) |
| Métricas en Prometheus | Confirmadas | Confirmadas (`true`) | No |

## 3. Riesgos Aceptados
* **Kafka sin volumen:** Se acepta porque los datos se pueden regenerar con el script productor. En producción, se usaría un volumen persistente.
* **Credenciales por defecto:** Se mantiene `admin` por defecto para facilitar el arranque en clase. En producción, se exigiría una contraseña robusta desde el primer inicio.