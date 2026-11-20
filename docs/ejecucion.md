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