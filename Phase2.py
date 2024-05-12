from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit
from pyspark.ml.recommendation import ALS
from pyspark.ml.feature import StringIndexer
from pyspark.sql.types import IntegerType
import numpy as np
from annoy import AnnoyIndex

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

        # Split data into training and testing sets
        trainingData, testData = df.randomSplit([0.8, 0.2], seed=1234)

        # Train ALS model
        als = ALS(rank=10, maxIter=10, regParam=0.01, userCol="id", itemCol="audio_file_index", implicitPrefs=True)
        model = als.fit(trainingData)

        print("Model training completed successfully.")

        # Save the trained model
        model.save("model_path")

        # Save the split data
        trainingData.write.format("parquet").save("training_data_path")
        testData.write.format("parquet").save("test_data_path")

    except Exception as e:
        print("An error occurred during model training:", e)

    finally:
        spark.stop()

# Function to generate random track embeddings (replace this with your actual data loading code)
def generate_random_embeddings(num_tracks, embedding_dim):
    return [np.random.rand(embedding_dim) for _ in range(num_tracks)]

# Function to build the Annoy index in chunks
def build_ann_index_in_chunks(track_embeddings, chunk_size=4000, num_trees=100):
    embedding_dim = len(track_embeddings[0])
    num_tracks = len(track_embeddings)
    annoy_index = AnnoyIndex(embedding_dim, 'angular')  # Angular distance is suitable for cosine similarity

    # Build the index in chunks
    for i in range(0, num_tracks, chunk_size):
        chunk_end = min(i + chunk_size, num_tracks)
        for j, embedding in enumerate(track_embeddings[i:chunk_end]):
            annoy_index.add_item(i + j, embedding)
        print("Built index for chunk {} to {}".format(i, chunk_end))
    print("\n\n")
    annoy_index.build(num_trees)
    return annoy_index

# Function to save the Annoy index to disk
def save_ann_index(ann_index, index_filename):
    ann_index.save(index_filename)

# Function to load the Annoy index from disk
def load_ann_index(index_filename, embedding_dim):
    ann_index = AnnoyIndex(embedding_dim, 'angular')
    ann_index.load(index_filename)
    return ann_index

# Function to perform nearest neighbor search using the Annoy index
def find_nearest_neighbors(ann_index, track_id, num_neighbors=5):
    nearest_neighbor_ids = ann_index.get_nns_by_item(track_id, num_neighbors)
    return nearest_neighbor_ids

if __name__ == "__main__":
    # State the input and output directories of your Database 
    input_uri = "mongodb://localhost:27017/project.tashi"
    output_uri = "mongodb://localhost:27017/project.tashi"

    # Train the music recommendation model
    train_music_recommendation_model(input_uri, output_uri)

    # Generate random track embeddings (replace this with your actual data loading code)
    num_tracks = 106574  # Number of tracks
    embedding_dim = 128  # Dimensionality of track embeddings
    track_embeddings = generate_random_embeddings(num_tracks, embedding_dim)

    # Build Annoy index in chunks
    ann_index = build_ann_index_in_chunks(track_embeddings, chunk_size=10000, num_trees=100)

    # Save Annoy index to disk
    index_filename = 'track_annoy_index.ann'
    save_ann_index(ann_index, index_filename)

    # Later, you can load the index from disk
    ann_index_loaded = load_ann_index(index_filename, embedding_dim)

    # Prompt the user to input a track ID
    while True:
        try:
            track_id = int(input("Enter a track ID (0 to {}): ".format(num_tracks - 1)))
            if track_id < 0 or track_id >= num_tracks:
                raise ValueError("Track ID must be between 0 and {}".format(num_tracks - 1))
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    # Perform nearest neighbor search for the input track ID
    num_neighbors = 20
    nearest_neighbor_ids = find_nearest_neighbors(ann_index_loaded, track_id, num_neighbors)
    print("Nearest neighbor IDs of track {}: {}".format(track_id, nearest_neighbor_ids))

