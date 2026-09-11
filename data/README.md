# Datos – EcoData Juliaca

Los archivos CSV se obtienen de Open-Meteo:

## Clima histórico
- API: https://archive-api.open-meteo.com/v1/archive
- Coordenadas: latitude=-15.5, longitude=-70.13333
- Variables: temperature_2m, wind_speed_10m, wind_direction_10m, relative_humidity_2m
- Formato: CSV

## Calidad del aire
- API: https://air-quality-api.open-meteo.com/v1/air-quality
- Variables: pm10, pm2_5, european_aqi, us_aqi

Colocar los archivos descargados en esta carpeta o montarlos en `/opt/ecodata/data/` dentro del contenedor Docker.