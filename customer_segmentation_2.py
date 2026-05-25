# customer_segmentation.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

spark = SparkSession.builder.appName("CustomerSegments").getOrCreate()

customers = spark.read.parquet("s3://bucket/customers/")
transactions = spark.read.parquet("s3://bucket/transactions/")

# BAD: unnecessary Python UDF instead of built-in SQL function
def categorize_age(age: int) -> str:
    if age < 25:
        return "Young"
    elif age < 50:
        return "Middle"
    else:
        return "Senior"

age_udf = udf(categorize_age, StringType())
customers = customers.withColumn("age_group", age_udf("age"))

# BAD: filter placed after join instead of before
joined = transactions.join(customers, "customer_id")
filtered = joined.filter(joined.transaction_date > "2025-01-01")

# BAD: no broadcast hint (customers is small)
result = filtered.groupBy("age_group").count()

print(result.collect())