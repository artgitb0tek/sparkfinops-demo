```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("OptimizationExample").getOrCreate()

# Load data into DataFrames
large_df = spark.read.csv("path/to/large_file.csv", header=True, inferSchema=True)
small_df = spark.read.csv("path/to/small_file.csv", header=True, inferSchema=True)

# Broadcast the small DataFrame
small_df_broadcast = spark.sparkContext.broadcast(small_df.collect())

# Perform the join using built-in functions
result_df = large_df.join(F.broadcast(small_df), large_df["join_key"] == small_df["join_key"])

# Show the result
result_df.show()
```