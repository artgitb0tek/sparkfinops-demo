# sales_aggregation.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast

spark = SparkSession.builder.appName("SalesAgg").getOrCreate()

orders = spark.read.parquet("s3://bucket/orders/")
customers = spark.read.parquet("s3://bucket/customers/")

# Broadcast hint for small table
# Bad: groupByKey instead of reduceByKey, no broadcast
joined = orders.join(customers, "customer_id", "inner")
rdd = joined.rdd.map(lambda row: (row["product_id"], row["amount"]))
result = rdd.groupByKey().mapValues(sum).collect()
print(result)

