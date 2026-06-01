# sales_aggregation.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast

spark = SparkSession.builder.appName("SalesAgg").getOrCreate()

# Bad version: no broadcast hint, groupByKey instead of reduceByKey
orders = spark.read.parquet("s3://bucket/orders/")
customers = spark.read.parquet("s3://bucket/customers/")
joined = orders.join(customers, "customer_id", "inner")
rdd = joined.rdd.map(lambda row: (row["product_id"], row["amount"]))
result = rdd.groupByKey().mapValues(sum).collect()
print(result)