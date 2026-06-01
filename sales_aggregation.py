```python
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast

sc = SparkContext.getOrCreate()
spark = SparkSession(sc)

# Load data
large_rdd = sc.textFile("path/to/large_file.txt")
small_rdd = sc.textFile("path/to/small_file.txt")

# Perform join operation with broadcasting
small_rdd_broadcasted = broadcast(small_rdd.collectAsMap())
joined_rdd = large_rdd.map(lambda x: (x.split(",")[0], x)).join(small_rdd_broadcasted.value)

# Further processing...
```