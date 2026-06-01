```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast

spark = SparkSession.builder.appName("OptimizationExample").getOrCreate()

# Load large DataFrame
large_df = spark.read.csv("path/to/large_file.csv", header=True, inferSchema=True)

# Load small DataFrame
small_df = spark.read.csv("path/to/small_file.csv", header=True, inferSchema=True)

# Use broadcast hint for the small DataFrame to optimize the join operation
result_df = large_df.join(broadcast(small_df), on="join_column", how="inner")

# Perform further transformations and actions
result_df.show()
```