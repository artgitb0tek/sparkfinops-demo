# sales_aggregation.py
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("SalesAgg").getOrCreate()

orders = spark.read.parquet("s3://bucket/orders/")
customers = spark.read.parquet("s3://bucket/customers/")

# BAD: no broadcast hint – will cause a full shuffle join
joined = orders.join(customers, "customer_id", "inner")

# BAD: groupByKey + mapValues instead of reduceByKey
rdd = joined.rdd.map(lambda row: (row["product_id"], row["amount"]))
result = rdd.groupByKey().mapValues(sum)

# BAD: excessive repartition (2000 partitions) will cause huge shuffle
result_repartitioned = result.repartition(2000)

# (optional) trigger an action
print(result_repartitioned.collect())