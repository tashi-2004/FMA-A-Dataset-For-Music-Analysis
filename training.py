from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.recommendation import ALS
from pyspark.ml.feature import StringIndexer
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import col, lit 

def train_music_recommendation_model(input_uri, output_uri):
    # Create a SparkSession
    spark = SparkSession.builder \
        .appName("MusicRecommendation") \
        .config("spark.mongodb.input.uri", input_uri) \
        .config("spark.mongodb.output.uri", output_uri) \
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
        .config("spark.driver.memory", "8g") \
        .config("spark.network.timeout", "600s") \
        .getOrCreate()

    try:
        print("Starting model training...")
        
        # Read data from MongoDB
        df = spark.read.format("mongo").load()

        # Generate a unique identifier column within the integer range supported by ALS
        df = df.rdd.zipWithIndex().toDF(["data", "id"]).select(col("id").cast(IntegerType()), col("data.*"))

        # Convert audio_file column to numeric using StringIndexer
        indexer = StringIndexer(inputCol="audio_file", outputCol="audio_file_index")
        df = indexer.fit(df).transform(df)

        # Treat interactions as implicit feedback (e.g., whether a user listened to a song)
        # Use a constant value to indicate positive interactions
        # Here, we assume that each interaction is a positive preference
        # You can adjust this based on your specific scenario
        df = df.withColumn("rating", lit(1))

        # Train ALS model
        als = ALS(rank=10, maxIter=10, regParam=0.01, userCol="id", itemCol="audio_file_index", implicitPrefs=True)
        model = als.fit(df)

        print("Model training completed successfully.")

        # Optionally, evaluate the model on the test set or make recommendations

    except Exception as e:
        print("An error occurred during model training:", e)

    finally:
        spark.stop()

# State the input and output directories of your Database 
input_uri = "mongodb://localhost:27017/project.tashi"
output_uri = "mongodb://localhost:27017/project.tashi"

# Train the music recommendation model
train_music_recommendation_model(input_uri, output_uri)
