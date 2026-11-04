@echo off
REM EcoData U2 - detiene sin borrar nada (conserva volumenes e historico de Prometheus/Grafana).
chcp 65001 >nul
docker stop lambda26-prometheus lambda26-grafana lambda26-pushgateway lambda26-pyspark
cd /d D:\ACUÑA\lambda26-bigdata
cd obs && docker compose stop && cd ..
cd kafka && docker compose stop && cd ..
echo Detenido. Los datos se conservan. NUNCA uses "docker compose down -v" ni "docker volume prune".
pause
