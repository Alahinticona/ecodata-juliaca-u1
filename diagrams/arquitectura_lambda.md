# Arquitectura Lambda – EcoData

```mermaid
flowchart LR
    Fuente["Open-Meteo<br/>Clima + Calidad del Aire"]
    
    subgraph Batch["Ruta Batch (Unidad 1)"]
        PySpark["PySpark<br/>Limpieza + Calidad"]
        Gold["Parquet Gold<br/>particionado"]
        ML["Spark MLlib<br/>Modelo de regresión"]
    end
    
    subgraph Speed["Ruta Speed (Unidad 2)"]
        Kafka["Kafka"]
        Streaming["Spark Structured Streaming"]
        Alertas["Alertas tempranas"]
    end
    
    Fuente --> PySpark --> Gold --> ML
    Fuente --> Kafka --> Streaming --> Alertas