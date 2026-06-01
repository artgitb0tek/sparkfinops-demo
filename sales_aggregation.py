```python
from pyspark import SparkContext
from pyspark.sql import SparkSession

sc = SparkContext.getOrCreate()
spark = SparkSession(sc)

# Sample data
data1 = [("a", 1), ("b", 2), ("a", 3), ("b", 4)]
data2 = [("a", 5), ("b", 6)]

# Create RDDs
rdd1 = sc.parallelize(data1)
rdd2 = sc.parallelize(data2)

# Use reduceByKey instead of groupByKey
reduced_rdd = rdd1.reduceByKey(lambda x, y: x + y)

# Broadcast the smaller RDD for the join
broadcast_rdd2 = sc.broadcast(rdd2.collectAsMap())

# Perform join using the broadcasted variable
joined_rdd = reduced_rdd.map(lambda x: (x[0], (x[1], broadcast_rdd2.value.get(x[0], 0))))

# Collect results
results = joined_rdd.collect()
print(results)
```