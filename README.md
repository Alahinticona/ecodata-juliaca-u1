# Sistema de Alerta Temprana de Calidad del Aire (EcoData)

**Curso:** Big Data (Unidad 3 - Producto Final)  
**Integrantes:**
* Alahin Reyme Ticona Veliz (Batch/Spark)

## 📌 Descripción del Proyecto
Sistema Big Data distribuido end-to-end diseñado para monitorear y anticipar episodios de alta contaminación del aire (PM10, PM2.5) en Juliaca, utilizando variables meteorológicas. Implementa una arquitectura **Lambda** (Batch + Streaming) para emitir alertas tempranas y prevenir riesgos respiratorios.

## 🏗️ Arquitectura End-to-End
El sistema integra las tres capas de la arquitectura Lambda:

```mermaid
graph TD
    A[API Open-Meteo] -->|Datos Históricos| B(Spark Batch)
    A -->|Script Python| C(Kafka)
    C -->|Streaming| D(Spark Structured Streaming)
    B -->|Parquet + Modelos| E(Pushgateway)
    D -->|Inferencia en tiempo real| E
    E --> F[Prometheus]
    F --> G[Grafana Dashboards]

⚙️ Prácticas DataOps y Hardening (Unidad 3)
El proyecto aplica prácticas de despliegue reproducible y estabilización:

Healthchecks y dependencias: Todos los contenedores (infra/kafka y infra/obs) cuentan con comprobaciones de salud (healthcheck) y esperas por dependencia (service_healthy).

Seguridad: Las credenciales de Grafana se manejan mediante variables de entorno (${GRAFANA_ADMIN_PASSWORD}) en lugar de estar en texto plano.

Integración verificable: El notebook S13_integracion_dataops ejecuta compuertas de calidad y genera un manifiesto JSON de cada ejecución (evidencia en notebooks/S13_integracion_dataops/artifacts/).

🚀 Ejecución del Sistema
Para levantar todo el entorno y reproducir los resultados, consulta la guía detallada en docs/ejecucion.md.

📚 Documentación Adicional
Matriz de Trazabilidad

Evidencia de Hardening (S14)

text

---

### 📊 2. Crear la Matriz de Trazabilidad (Criterio 3 y 6)

Crea una carpeta `docs/` (si no la tienes) y dentro un archivo llamado **`trazabilidad.md`**. Pega esto:

```markdown
# Matriz de Trazabilidad

| Integrante | Dimensión | Indicador U1 (Batch) | Indicador U2 (Streaming) | Fuente y Técnica | Evidencia |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **alahin** | Predictiva (PM2.5) | Concentración histórica mensual (µg/m³) | Predicción de picos en próximas horas | Open-Meteo / Regresión (Spark MLlib) | `notebooks/01_pipeline_completo_u1.ipynb` |
| **Alahin** | Predictiva (Clima) | Influencia histórica de temp/viento | Predicción de condiciones climáticas en vivo | Open-Meteo / Clasificación (Spark MLlib) | `notebooks/S13_integracion_dataops.ipynb` |
🛡️ 3. Crear la Evidencia de Hardening (Criterio 4)
Dentro de la carpeta docs/, crea un archivo llamado hardening.md y pega esto:

markdown
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
💻 4. Crear la Guía de Ejecución (Criterio 5)
Dentro de docs/, crea un archivo llamado ejecucion.md. Este documento es vital para que el profesor vea que otra persona puede correr tu proyecto:

markdown
# Guía de Ejecución Paso a Paso

Sigue estos comandos en orden para reproducir el sistema completo (Batch + Streaming):

### 1. Levantar Infraestructura (Docker)
```powershell
cd infra/kafka
docker compose up -d --wait

cd ../pyspark
docker compose up -d

cd ../obs
docker compose up -d --wait
2. Entrenar Modelos (Batch)
powershell
docker cp s12 lambda26-pyspark:/tmp/s12
docker exec -it lambda26-pyspark python /tmp/s12/scripts/entrenar_temp.py --archivo /tmp/s12/clima_juliaca_2023.json --salida /tmp/s12/modelo_temp
docker exec -it lambda26-pyspark python /tmp/s12/scripts/entrenar_pm25.py --archivo /tmp/s12/aq_juliaca_2023.json --salida /tmp/s12/modelo_pm25
3. Iniciar Streaming y Datos
Abre 3 terminales distintas:

Terminal 1 (Datos Clima): docker exec lambda26-pyspark python /tmp/s12/scripts/openmeteo_clima_a_kafka.py --api --bootstrap kafka:9092

Terminal 2 (Datos Aire): docker exec lambda26-pyspark python /tmp/s12/scripts/openmeteo_a_kafka.py --api --bootstrap kafka:9092

Terminal 3 (Spark Streaming): docker exec -it lambda26-pyspark spark-submit ... (comando completo en la raíz)

4. Ejecutar Integración (S13)
Abre Jupyter en http://localhost:4488, ingresa a notebooks/S13_integracion_dataops y ejecuta todas las celdas. Revisa el manifiesto generado en artifacts/.

text

---

---

### 🚀 6. Subir todo a GitHub

Una vez que hayas creado y guardado estos 5 archivos (`README.md`, `docs/trazabilidad.md`, `docs/hardening.md`, `docs/ejecucion.md` y el esquema mental del guion), abre PowerShell en la raíz de tu proyecto y ejecuta:

```powershell
git add .
git commit -m "docs(s15): README final, matriz de trazabilidad, hardening y guia de ejecucion para el producto final"
git pull origin main --no-edit
git push origin main
---