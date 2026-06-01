```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast

spark = SparkSession.builder.appName("OptimizationExample").getOrCreate()

# Load large DataFrame
large_df = spark.read.csv("path/to/large_file.csv", header=True, inferSchema=True)

# Load small DataFrame
small_df = spark.read.csv("path/to/small_file.csv", header=True, inferSchema=True)

# Perform join operation with broadcast
result_df = large_df.join(broadcast(small_df), on="join_key", how="inner")

# Show result
result_df.show()
```