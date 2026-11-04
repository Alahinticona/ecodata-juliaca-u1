@echo off
REM EcoData U2 - verificacion rapida del estado (equivale a "verificar_producto")
chcp 65001 >nul
echo === Contenedores ===
docker ps --format "table {{.Names}}\t{{.Status}}" | findstr lambda26
echo.
echo === Targets de Prometheus (busca "up") ===
curl -s http://localhost:49090/api/v1/targets | findstr /i "pushgateway health"
echo.
echo === Frescura (segundos desde el ultimo push) ===
curl -s "http://localhost:49090/api/v1/query?query=time()-push_time_seconds{instance=\"inferencia\"}"
echo.
echo === Alertas activas ===
curl -s http://localhost:49090/api/v1/alerts
echo.
pause
