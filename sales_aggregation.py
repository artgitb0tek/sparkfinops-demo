```python
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

conf = SparkConf().setAppName("OptimizationExample")
sc = SparkContext(conf=conf)
spark = SparkSession(sc)

# Load data
small_rdd = sc.textFile("small_data.txt")
large_rdd = sc.textFile("large_data.txt")

# Broadcast the small RDD
broadcasted_small_rdd = sc.broadcast(small_rdd.collectAsMap())

# Join operation using broadcasted variable
joined_rdd = large_rdd.map(lambda x: (x[0], x)).join(broadcasted_small_rdd.value)

# Use reduceByKey for aggregation
result_rdd = joined_rdd.map(lambda x: (x[0], x[1][0], x[1][1])) \
                        .reduceByKey(lambda a, b: (a[0], a[1] + b[1]))

# Save the result
result_rdd.saveAsTextFile("output.txt")

sc.stop()
```