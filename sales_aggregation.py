# sales_aggregation.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast

spark = SparkSession.builder.appName("SalesAgg").getOrCreate()

orders = spark.read.parquet("s3://bucket/orders/")
customers = spark.read.parquet("s3://bucket/customers/")

# Broadcast hint for small table
joined = orders.join(broadcast(customers), "customer_id", "inner")

# reduceByKey (efficient)
# Change the last part to:
rdd = joined.rdd.map(lambda row: (row["product_id"], row["amount"]))
result = rdd.groupByKey().mapValues(sum).collect()
print(result)