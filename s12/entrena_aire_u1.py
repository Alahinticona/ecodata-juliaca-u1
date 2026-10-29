"""EcoData U1 - Dimensión Aire (Lanzeloth). Modelo batch con Spark MLlib.
Objetivo: pronosticar PM2.5 a +1 h con el histórico de Open-Meteo (CAMS) de Juliaca.
Uso:  python entrena_aire_u1.py <ruta juliaca_calidad_aire.csv> <salida.json>
"""
import sys, json
from pyspark.sql import SparkSession, functions as F, Window
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression, RandomForestRegressor, GBTRegressor
from pyspark.ml.evaluation import RegressionEvaluator

csv, out = sys.argv[1], sys.argv[2]
spark = SparkSession.builder.master("local[2]").appName("ecodata-u1-aire").config("spark.ui.enabled", "false").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

# 1. Lectura (las 3 primeras líneas son metadatos) y esquema explícito
raw = spark.read.text(csv)
rows = raw.rdd.zipWithIndex().filter(lambda x: x[1] >= 3).map(lambda x: x[0][0])
df = (spark.read.csv(rows, header=True, inferSchema=False)
      .toDF("time", "pm10", "pm2_5", "eaqi", "usaqi"))
df = df.select(F.to_timestamp("time").alias("time"),
               *[F.col(c).cast("double").alias(c) for c in ["pm10", "pm2_5", "eaqi", "usaqi"]])
total = df.count()

# 2. Calidad: nulos, duplicados, rangos físicos
nulos = {c: df.filter(F.col(c).isNull()).count() for c in df.columns}
dups = total - df.dropDuplicates(["time"]).count()
limpio = df.dropDuplicates(["time"]).dropna(subset=["pm10", "pm2_5"]).filter((F.col("pm2_5") >= 0) & (F.col("pm10") >= 0))
n_limpio = limpio.count()

# 3. Nivel de riesgo (umbrales del proyecto)
limpio = limpio.withColumn("nivel_riesgo", F.when(F.col("pm2_5") >= 50, "Alto").when(F.col("pm2_5") >= 25, "Moderado").otherwise("Bajo"))
riesgo = {r["nivel_riesgo"]: r["count"] for r in limpio.groupBy("nivel_riesgo").count().collect()}

# 4. Variables: hora, mes, rezagos y media móvil (solo pasado) ; objetivo = pm2_5 en t+1
w = Window.orderBy("time")
d = (limpio.withColumn("hour", F.hour("time")).withColumn("month", F.month("time"))
     .withColumn("lag1", F.lag("pm2_5", 1).over(w)).withColumn("lag2", F.lag("pm2_5", 2).over(w))
     .withColumn("lag3", F.lag("pm2_5", 3).over(w))
     .withColumn("media6", F.avg("pm2_5").over(w.rowsBetween(-5, 0)))
     .withColumn("pm10_t", F.col("pm10"))
     .withColumn("objetivo", F.lead("pm2_5", 1).over(w))
     .dropna(subset=["lag1", "lag2", "lag3", "objetivo"]))
feats = ["pm2_5", "lag1", "lag2", "lag3", "media6", "pm10_t", "hour", "month"]
d = VectorAssembler(inputCols=feats, outputCol="features").transform(d).cache()

# 5. Partición temporal 80/20 (sin mezclar el futuro)
n = d.count(); k = int(n * 0.8)
ordered = d.orderBy("time").withColumn("rn", F.row_number().over(Window.orderBy("time")))
train = ordered.filter(F.col("rn") <= k).cache(); test = ordered.filter(F.col("rn") > k).cache()

ev = {m: RegressionEvaluator(labelCol="objetivo", predictionCol="prediction", metricName=m) for m in ["rmse", "mae", "r2"]}
res = {}
# línea base: persistencia (pm2_5 en t+1 = pm2_5 en t)
base = test.withColumn("prediction", F.col("pm2_5"))
res["Persistencia (base)"] = {m: ev[m].evaluate(base) for m in ev}
modelos = {
    "LinearRegression": LinearRegression(featuresCol="features", labelCol="objetivo"),
    "RandomForest": RandomForestRegressor(featuresCol="features", labelCol="objetivo", numTrees=100, maxDepth=8, seed=42),
    "GBT": GBTRegressor(featuresCol="features", labelCol="objetivo", maxIter=80, maxDepth=5, seed=42),
}
ajustados = {}
for nombre, est in modelos.items():
    mod = est.fit(train); ajustados[nombre] = mod
    pred = mod.transform(test)
    res[nombre] = {m: ev[m].evaluate(pred) for m in ev}
mejor = min((k_ for k_ in modelos), key=lambda k_: res[k_]["rmse"])
imp = None
if hasattr(ajustados[mejor], "featureImportances"):
    imp = dict(zip(feats, [float(x) for x in ajustados[mejor].featureImportances.toArray()]))

salida = {
    "registros_crudos": total, "registros_limpios": n_limpio, "nulos": nulos, "duplicados": dups,
    "periodo": [str(r) for r in (df.agg(F.min("time"), F.max("time")).first())],
    "riesgo": riesgo, "train": k, "test": n - k, "metricas": res, "mejor_modelo": mejor, "importancias": imp,
}
json.dump(salida, open(out, "w"), indent=2, ensure_ascii=False, default=str)
print(json.dumps(salida, indent=2, ensure_ascii=False, default=str))
spark.stop()
