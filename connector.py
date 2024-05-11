# Import necessary libraries 
from pyspark.sql import SparkSession

# State the input and output directories of your Database 
input_uri = "mongodb://localhost:27017/project.tashi"
output_uri = "mongodb://localhost:27017/project.tashi"

# Make a Spark session to use PySpark and also configure Spark to be connected with MongoDB
spark = SparkSession.builder \
    .appName("myProject") \
    .config("spark.mongodb.input.uri", input_uri) \
    .config("spark.mongodb.output.uri", output_uri) \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
    .getOrCreate()

# Read the data from MongoDB into a Spark DataFrame
df_read = spark.read.format("mongo").load()

# Display the DataFrame contents
df_read.show()

