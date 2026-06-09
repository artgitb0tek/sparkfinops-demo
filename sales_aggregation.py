# sales_aggregation.py
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("SalesAgg").getOrCreate()

orders = spark.read.parquet("s3://bucket/orders/")
customers = spark.read.parquet("s3://bucket/customers/")

joined = orders.join(F.broadcast(customers), "customer_id", "inner")

result = joined.groupBy("product_id").agg(F.sum("amount")).collect()
print(result)