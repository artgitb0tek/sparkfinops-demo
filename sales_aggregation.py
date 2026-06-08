# sales_aggregation.py
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("SalesAgg").getOrCreate()

orders = spark.read.parquet("s3://bucket/orders/")
customers = spark.read.parquet("s3://bucket/customers/")

# BAD: missing broadcast hint – causes expensive shuffle join
joined = orders.join(customers, "customer_id", "inner")

# BAD: groupByKey + mapValues instead of reduceByKey
rdd = joined.rdd.map(lambda row: (row["product_id"], row["amount"]))
result = rdd.groupByKey().mapValues(sum).collect()
print(result)