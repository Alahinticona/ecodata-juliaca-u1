# EcoData U2: levantar todo en tu laptop (Windows + Docker Desktop)

Pipeline: Open-Meteo -> Kafka -> Spark Structured Streaming -> Pushgateway -> Prometheus -> Grafana.
Aire (PM2.5) y clima (temperatura), predicción a +1 h con modelos MLlib.

Requisitos: Docker Desktop (Engine running), cargador conectado, 8 GB de RAM libres.
Todos los comandos son para **CMD**. `REPO` = carpeta donde clonaste/descargaste este repo.

## 1. Infraestructura (una sola vez, en este orden)

```
cd /d REPO\infra\kafka
docker compose up -d

cd /d REPO\infra\obs
docker compose up -d

cd /d REPO\infra\pyspark
copy .env.example .env
docker compose -f compose.yml -f compose.kafka.yml up -d --build
```

- Kafka va primero porque crea la red `lambda26-kafka-net`.
- `.env` debe tener `JUPYTER_TOKEN=lo-que-quieras` (Jupyter queda en http://localhost:4488).
- Comprueba: `docker ps` debe listar `lambda26-pyspark`, `lambda26-prometheus`, `lambda26-grafana`, `lambda26-pushgateway` y los contenedores de Kafka.
- Prometheus: http://localhost:49090/targets -> job `pushgateway` en UP.

## 2. Copiar scripts, datos y modelos al contenedor

```
cd /d REPO
docker exec lambda26-pyspark mkdir -p /tmp/s12
docker cp s12\scripts lambda26-pyspark:/tmp/s12/scripts
docker cp s12\aq_juliaca_2023.json lambda26-pyspark:/tmp/s12/aq_juliaca_2023.json
docker cp s12\clima_juliaca_2023.json lambda26-pyspark:/tmp/s12/clima_juliaca_2023.json
powershell -Command "Expand-Archive -Path 's12\modelos_s12.zip' -DestinationPath 's12\_modelos' -Force"
docker cp s12\_modelos\modelo_pm25 lambda26-pyspark:/tmp/s12/modelo_pm25
docker cp s12\_modelos\modelo_temp lambda26-pyspark:/tmp/s12/modelo_temp
```

Si prefieres reentrenar los modelos en vez de usar el .zip:

```
docker exec -it lambda26-pyspark python /tmp/s12/scripts/entrenar_pm25.py --archivo /tmp/s12/aq_juliaca_2023.json --salida /tmp/s12/modelo_pm25
docker exec -it lambda26-pyspark python /tmp/s12/scripts/entrenar_temp.py --archivo /tmp/s12/clima_juliaca_2023.json --salida /tmp/s12/modelo_temp
```

## 3. Dashboards en Grafana (se importan a mano)

http://localhost:43000 (usuario `admin`, clave `admin`) -> Dashboards -> New -> Import -> Upload JSON:

- `s12\grafana\dashboard_s12_ecodata.json`  (aire + clima, el principal)
- `s12\grafana\dashboard_s12_aire.json`
- `s12\dashboards\*.json`  (S9 y S11 de clima)

El datasource Prometheus ya se crea solo (provisioning).

## 4. Jobs de Spark (dos CMD, uno por job; no cerrar, no duplicar)

Aire:
```
docker exec -it lambda26-pyspark spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.2.0 /tmp/s12/scripts/s12_streaming_aire.py --modelo /tmp/s12/modelo_pm25 --limpiar
```
Clima:
```
docker exec -it lambda26-pyspark spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.2.0 /tmp/s12/scripts/s12_streaming_clima.py --modelo /tmp/s12/modelo_temp --limpiar
```
Espera ~40-60 s. Los jobs no imprimen por lote: se verifica en Grafana / Pushgateway.

## 5. Publicadores (otros dos CMD)

Replay del archivo, un evento cada 20 s (744 eventos = 4 h 8 min):
```
docker exec lambda26-pyspark python /tmp/s12/scripts/openmeteo_a_kafka.py --archivo /tmp/s12/aq_juliaca_2023.json --desde 2023-12-01T00:00 --pausa 20
docker exec lambda26-pyspark python /tmp/s12/scripts/openmeteo_clima_a_kafka.py --archivo /tmp/s12/clima_juliaca_2023.json --desde 2023-12-01T00:00 --pausa 20
```
Demo rápida: `--pausa 0.05`.
Datos recientes por API: añade `--api` (sin --archivo). Dato tardío para el watermark: `--api --tardio 30`.

Las predicciones y el MAE aparecen tras 25 eventos (el modelo necesita 24 h de historia).

## 6. Enlaces

| Servicio | URL |
|---|---|
| Grafana | http://localhost:43000 |
| Prometheus | http://localhost:49090 |
| Pushgateway | http://localhost:49091/metrics |
| Kafka UI | http://localhost:48085 |
| Jupyter | http://localhost:4488 |

## 7. Notebooks

`notebooks\u2_aire` y `notebooks\u2_clima`. Para ejecutarlos dentro del contenedor, copia la carpeta a `infra\pyspark\sesiones\` (se monta como `/opt`).

## Apagar

Ctrl+C en cada job y publicador. Luego `docker compose down` en cada carpeta de `infra\`.
