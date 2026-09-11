# Laboratorio PySpark

Entorno local para ejecutar los notebooks del curso con Spark y Jupyter.

## Clonar

```bash
git clone https://github.com/262bigdata/lambda26.git
cd lambda26/pyspark
```

## Carpetas

`pyspark/` separa la **configuración** (lo que arma el entorno) del
**contenido** (lo que el curso produce):

- `Dockerfile`, `compose.yml`, `.env`/`.env.example`, `README.md`: solo se
  usan desde el host, para levantar el contenedor — no se montan dentro de
  él, así que nunca aparecen en el explorador de archivos de Jupyter.
- `sesiones/`: la única carpeta que se monta dentro del contenedor (en
  `/opt`). Ahí vive todo lo demás.

Dentro de `sesiones/`, cada sesión que necesita datos reales tiene su propia
carpeta autocontenida (`sXX-nombre/`): el notebook, sus datos de entrada
(`data/`, si el dataset viene de varios archivos) y sus salidas
(`artifacts/`, si la sesión genera resultados). No hay una carpeta
`data/`/`artifacts/` compartida entre sesiones — cada una tiene la suya.

- `sesiones/s01-arquitectura/`: notebook y dataset (`data/biblia_ntv_.csv`) de S1.
- `sesiones/s02-fundamentos/`: notebook y dataset (`data/`, dataset H&M) de S2.
- `sesiones/s03-procesamiento-calidad-datos/`: notebook y dataset (`data/`,
  mismo H&M de S2: `customers.csv`/`articles.csv`) de S3.
- `sesiones/s03-parte2-transacciones/`: notebook opcional (S3 parte 2) que
  prepara `transactions.parquet` (H&M) particionado por mes, como entrada
  directa de S4.
- Sesiones futuras agregan su propia carpeta (`sesiones/s04-...`,
  `sesiones/s05-...`) a medida que el curso avanza.

## Uso

Desde `lambda26/pyspark`, copia las variables de entorno (una sola vez):

```powershell
cp .env.example .env
```

Luego levanta el laboratorio:

```powershell
docker compose up -d
```

La integración con Kafka (módulo `kafka/` y el override
`pyspark/compose.kafka.yml`) todavía no existe en este repositorio: se crea
recién en la Unidad 2 (S6), cuando el curso pasa de batch a streaming. Hasta
entonces, este entorno corre solo (PySpark + Jupyter, sin Kafka).

Luego abre JupyterLab:

```text
http://localhost:4488/lab?token=sintoken
```

Tambien puedes entrar a Jupyter Notebook:

```text
http://localhost:4488/?token=sintoken
```

**Nota:** el `Dockerfile` arranca el contenedor con `jupyter notebook`, no `jupyter lab` — igual puedes entrar a `/lab` porque `notebook` 7.x viene construido sobre el mismo servidor de JupyterLab y sirve ambas interfaces (`/lab` y `/tree`) desde el mismo proceso. No es necesario cambiar el comando para usar `/lab`.

Spark UI queda en:

```text
http://localhost:4042
```

**Nota:** Spark usa el puerto 4040 por defecto, pero `compose.yml` lo expone en tu máquina como `4042` (`"4042:4040"`) — dentro del contenedor sigue siendo 4040, solo cambia el puerto con el que accedes desde el navegador. Esto evita choques con otros servicios que puedan estar usando el 4040 en tu máquina.

La carpeta `sesiones/` se monta de una sola vez dentro del contenedor en
`/opt` (`compose.yml`: `./sesiones:/opt`) — por eso cada carpeta de sesión
aparece directamente como `/opt/sXX-nombre/`, sin mounts adicionales que
configurar cuando agregas una sesión nueva. Por ejemplo,
`sesiones/s02-fundamentos/data/` queda disponible en
`/opt/s02-fundamentos/data/`. Los archivos de configuración (`Dockerfile`,
`compose.yml`, etc.) se quedan fuera de este mount a propósito, para que no
aparezcan en el explorador de archivos de Jupyter.

### Alternativa con imagen oficial de PySpark + Jupyter

Tambien puedes levantar un entorno PySpark directamente con la imagen oficial
[`jupyter/pyspark-notebook`](https://hub.docker.com/r/jupyter/pyspark-notebook). Diferencia de peso: la imagen
personalizada de `lambda26` pesa ~1.9 GB, mientras que `jupyter/pyspark-notebook`
pesa ~6.9 GB — considera tu espacio en disco antes de elegir esta alternativa:

```yaml
# compose.yml
services:
    pyspark:
        image: jupyter/pyspark-notebook
        ports:
            - 4489:8888
            - 4041:4040
        environment:
            - JUPYTER_TOKEN=sintoken
        volumes:
            - ./:/home/jovyan
```

Puertos distintos a los de `compose.yml` (4488/4042) para poder levantar ambos entornos sin conflicto si hiciera falta.

Para levantar este entorno:

```powershell
docker compose up -d
```

Luego accede a JupyterLab:

```text
http://localhost:4489/lab?token=sintoken
```

O usa Jupyter Notebook:

```text
http://localhost:4489/?token=sintoken
```

## Notebooks

Los notebooks se crean progresivamente, uno por sesión, a medida que el
curso avanza (verificación mínima en S1, fundamentos en S2, calidad de
datos y formatos analíticos particionados en S3, ML distribuido en S4,
streaming e inferencia desde S8-S10) — cada uno dentro de la carpeta de su
propia sesión (`sesiones/sXX-nombre/`), junto a sus datos de entrada. Las
sesiones que todavía no tienen contenido no tienen carpeta creada.
