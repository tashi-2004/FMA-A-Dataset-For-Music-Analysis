from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import StringIndexer
from pyspark.sql.types import IntegerType
import numpy as np
from annoy import AnnoyIndex
import shutil
def train_music_recommendation_model(input_uri, output_uri):
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
        indexer = StringIndexer(inputCol="audio_file", outputCol="audio_file_index")
        df = indexer.fit(df).transform(df)
        df = df.rdd.zipWithIndex().toDF(["data", "id"]).select(col("id").cast(IntegerType()), col("data.*"))

        # Generate random embeddings (Replace this with your actual data loading code)
        num_tracks = df.count()  # Number of tracks
        embedding_dim = 128  # Dimensionality of track embeddings
        track_embeddings = generate_random_embeddings(num_tracks, embedding_dim)

        # Build Annoy index
        ann_index = build_ann_index(track_embeddings)

        index_filename = 'track_annoy_index.ann'
        # Remove existing index file if exists
        shutil.rmtree(index_filename, ignore_errors=True)
        save_ann_index(ann_index, index_filename)

        print("Model training completed successfully.")

    except Exception as e:
        print("An error occurred during model training:", e)

    finally:
        spark.stop()

# Placeholder function to generate random track embeddings
def generate_random_embeddings(num_tracks, embedding_dim):
    return [np.random.rand(embedding_dim) for _ in range(num_tracks)]

# Function to build the Annoy index
def build_ann_index(track_embeddings, num_trees=500):
    ann_index = AnnoyIndex(track_embeddings[0].shape[0], 'angular')
    for i, embedding in enumerate(track_embeddings):
        ann_index.add_item(i, embedding)
    ann_index.build(num_trees)
    return ann_index

# Function to save the Annoy index to disk
def save_ann_index(ann_index, index_filename):
    ann_index.save(index_filename)

# Function to perform nearest neighbor search using the Annoy index
def find_nearest_neighbors(ann_index, track_id, num_neighbors=5):
    return ann_index.get_nns_by_item(track_id, num_neighbors)

if __name__ == "__main__":
    # State the input and output directories of your Database 
    input_uri = "mongodb://localhost:27017/assignment.tashi"
    output_uri = "mongodb://localhost:27017/assignment.tashi"

    # Train the music recommendation model
    train_music_recommendation_model(input_uri, output_uri)
    

def generate_random_embeddings(num_tracks, embedding_dim):
    return [np.random.rand(embedding_dim) for _ in range(num_tracks)]   #returns the list of random embeddings


def build_ann_index_in_chunks(track_embeddings, chunk_size=2000, num_trees=500):
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
    while True:
        # Generate random track embeddings (replace this with your actual data loading code)
        num_tracks = 106574  # Number of tracks
        embedding_dim = 128  # Dimensionality of track embeddings
        track_embeddings = generate_random_embeddings(num_tracks, embedding_dim)

        # Build Annoy index in chunks
        ann_index = build_ann_index_in_chunks(track_embeddings, chunk_size=2000, num_trees=500)

        # Save Annoy index to disk
        index_filename = 'track_annoy_index.ann'
        save_ann_index(ann_index, index_filename)

        # Later, you can load the index from disk
        ann_index_loaded = load_ann_index(index_filename, embedding_dim)

        # Prompt the user to input a track ID
        while True:
            try:
                print("\t\t\t\t\t___________________")
                print("\t\t\t\t\t|  ANN ALGORITHM  |")
                print("\t\t\t\t\t|_________________|")
                print("\n\n")
                track_id = int(input("Enter a track ID (0 to {}): ".format(num_tracks - 1)))
                print("\n\n")
                if track_id < 0 or track_id >= num_tracks:
                    raise ValueError("Track ID must be between 0 and {}".format(num_tracks - 1))
                break
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

        # Perform nearest neighbor search for the input track ID
        num_neighbors = 50
        nearest_neighbor_ids = find_nearest_neighbors(ann_index_loaded, track_id, num_neighbors)
        print("Nearest neighbor IDs of track {}: {}".format(track_id, nearest_neighbor_ids))

        # Ask the user if they want to continue
        while True:
            print('\n')
            choice = input("Do you want to search again? (yes/no): ").lower()
            if choice in ['yes', 'no', 'y', 'n']:
                break
            else:
                print("Invalid choice. Please enter 'yes' or 'no'.")
        if choice == 'no':
            break


