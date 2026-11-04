@echo off
REM EcoData U2 - levanta SOLO la infraestructura. No borra volumenes ni datos.
chcp 65001 >nul
echo [1/5] Verificando Docker...
docker info >nul 2>&1 || (echo Docker Desktop no esta listo. Abrelo, espera a que diga "running" y vuelve a ejecutar. & pause & exit /b 1)
cd /d D:\ACUÑA\lambda26-bigdata || (echo No encuentro la carpeta del proyecto & pause & exit /b 1)
echo [2/5] Kafka...
cd kafka && docker compose up -d && cd ..
echo [3/5] Observabilidad (Prometheus, Grafana, kafka-exporter)...
cd obs && docker compose up -d && cd ..
echo [4/5] PySpark/Jupyter y Pushgateway...
docker start lambda26-pyspark lambda26-pushgateway
echo [5/5] Reiniciando Prometheus para cargar la configuracion y las alertas...
docker restart lambda26-prometheus
echo.
echo LISTO. Abre:
echo   Jupyter     http://localhost:4488
echo   Grafana     http://localhost:43000/d/lambda26-s12-ecodata   (admin / admin)
echo   Prometheus  http://localhost:49090/targets  y  /alerts
echo   Kafka UI    http://localhost:48085
echo.
echo Ahora en Jupyter: s12-ecodata/12_ecodata_u2.ipynb
pause
