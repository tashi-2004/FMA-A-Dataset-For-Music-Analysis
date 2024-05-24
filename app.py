from flask import Flask, jsonify, render_template, request, send_from_directory
from confluent_kafka import Producer, Consumer, KafkaException
import json
import os
from audioread.exceptions import NoBackendError
from pyspark.ml.feature import Normalizer, StringIndexer, VectorAssembler
from pyspark.ml.linalg import Vectors, VectorUDT
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
import librosa
from annoy import AnnoyIndex

def extract_mfcc(audio_path):
    try:
        audio, sample_rate = librosa.load(audio_path, sr=None)
        mfcc_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=100).mean(axis=1)
        return mfcc_features.tolist()
    except NoBackendError as e:
        print("No suitable audio backend found:", e)

def load_data_from_mongodb(spark_session, input_uri):
    df = spark_session.read.format("com.mongodb.spark.sql.DefaultSource").option("uri", input_uri).load()
    return df

array_to_vector_udf = udf(lambda arr: Vectors.dense(arr), VectorUDT())
def create_feature_vector(df):
    df = df.withColumn("features", array_to_vector_udf(df["mfcc_features"]))
    return df

def normalize_features(df):
    normalizer = Normalizer(inputCol="features", outputCol="normalized_features")
    df = normalizer.transform(df)
    return df

def load_trained_annoy_index():
    annoy_index = AnnoyIndex(100, 'angular')
    annoy_index.load('music_recommendation.ann')
    return annoy_index

def add_user_id_column(df, user_id_column):
    indexer = StringIndexer(inputCol=user_id_column, outputCol="user_id")
    indexed_df = indexer.fit(df).transform(df)
    return indexed_df

def find_nearest_neighbors(annoy_index, target_vector, k=10):
    nearest_neighbors = annoy_index.get_nns_by_vector(target_vector, k)
    return nearest_neighbors

input_uri = "mongodb://localhost:27017/bda.audio_features"

spark = SparkSession.builder \
    .appName("MusicRecommendationModel") \
    .config("spark.mongodb.input.uri", input_uri) \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.2") \
    .getOrCreate()

def process_audio_file(audio_path):
    audio_features = extract_mfcc(audio_path)
    audio_features_df = spark.createDataFrame([(audio_path, audio_features)], ["audio_path", "mfcc_features"])
    audio_features_df = create_feature_vector(audio_features_df)
    audio_features_df = normalize_features(audio_features_df)
    return audio_features_df

df = load_data_from_mongodb(spark, input_uri)
df.show()

df = create_feature_vector(df)
df.show()

df = normalize_features(df)
df.show()

df = add_user_id_column(df, "audio_path")
df.show()

selected_train_data = df.select("user_id", "normalized_features", "audio_path")
selected_train_data = selected_train_data.withColumnRenamed("normalized_features", "features")
selected_train_data.show()



app = Flask(__name__)

@app.route('/DataSet/<folder_number>/<filename>')
def serve_mp3_file(folder_number, filename):
    folder_number = str(folder_number).zfill(3)
    directory_path = f'DataSet/{folder_number}/'
    return send_from_directory(directory_path, filename)

@app.route('/covers/<filename>')
def serve_cover_image(filename):
    return send_from_directory('templates/covers/', filename)

# Kafka configuration
KAFKA_BROKER_URL = 'localhost:9092'  # Adjust if needed
REQUEST_TOPIC = 'audio_request_topic'
RESPONSE_TOPIC = 'audio_response_topic'

# Configure Kafka Producer
producer_config = {
    'bootstrap.servers': KAFKA_BROKER_URL,
}
producer = Producer(**producer_config)

# Configure Kafka Consumer
consumer_config = {
    'bootstrap.servers': KAFKA_BROKER_URL,
    'group.id': 'flask-group',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(**consumer_config)
consumer.subscribe([RESPONSE_TOPIC])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    audio_path = request.form.get('audio_path')
    producer.produce(REQUEST_TOPIC, audio_path)
    producer.flush()
    return jsonify({'status': 'processing', 'path': audio_path})

@app.route('/get_neighbors', methods=['POST'])
def get_neighbors():
    data = request.json
    audio_path = data.get('audio_path')

    try:
        audio_features_df = process_audio_file(audio_path)
        target_features = audio_features_df.collect()[0]["features"]
        annoy_index = load_trained_annoy_index()
        nearest_neighbors = find_nearest_neighbors(annoy_index, target_features, k=10)
        neighbors_data = selected_train_data.select("audio_path").collect()
        nearest_neighbor_paths = [neighbors_data[i]["audio_path"] for i in nearest_neighbors]
        html_li_elements = []
        for neighbor_path in nearest_neighbor_paths:
            name = os.path.basename(neighbor_path)
            html_li_elements.append(f'<li data-path="{neighbor_path}" data-name="{name}">{name}</li>')
        html_ul = '<ul>{}</ul>'.format("".join(html_li_elements))
        return jsonify({'status': 'success', 'html_ul': html_ul})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
if __name__ == '__main__':
    print("Running Flask on http://localhost:5000")
    app.run(debug=False)
