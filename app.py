from flask import Flask, render_template, request
import os
import json
import time
import librosa
import random
from kafka import KafkaProducer, KafkaConsumer

app = Flask(__name__)

# Kafka broker address
bootstrap_servers = 'localhost:9092'

# Kafka topic to publish and consume music recommendations
topic = 'tashi'

# Path to the directory containing the dataset
dataset_path = '/home/laibu/Downloads/fma_large'

# Function to extract audio features
def extract_features(audio_file):
    try:
        y, sr = librosa.load(audio_file)
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        rms = librosa.feature.rms(y=y)
        return {
            'file_path': audio_file,
            'tempo': float(tempo),
            'beats': beats.tolist(),
            'chroma_stft': chroma_stft.tolist(),
            'rms': rms.tolist()
        }
    except Exception as e:
        print(f"Error processing file {audio_file}: {e}")
        return None

# Function to generate music recommendations for each directory
def generate_recommendations():
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                             value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'))
    for i in range(156):
        directory = f"{i:03d}"
        directory_path = os.path.join(dataset_path, directory)
        if os.path.isdir(directory_path):
            print(f"Processing directory: {directory_path}")
            audio_files = [f for f in os.listdir(directory_path) if f.endswith('.mp3')]
            selected_files = random.sample(audio_files, min(5, len(audio_files)))
            for file_name in selected_files:
                file_path = os.path.join(directory_path, file_name)
                features = extract_features(file_path)
                if features:
                    producer.send(topic, value=features)
            time.sleep(1)
    producer.close()

# Function to apply recommendations based on features
def apply_recommendations():
    consumer = KafkaConsumer(topic,
                             bootstrap_servers=bootstrap_servers,
                             value_deserializer=lambda v: json.loads(v.decode('utf-8')))
    for message in consumer:
        features = message.value
        # Here you can implement the logic to apply recommendations based on the features received
        # For demonstration, let's just print the features
        print("Received features:", features)
    consumer.close()

# Define the 'recommend' route to handle form submission
@app.route('/recommend', methods=['POST'])
def recommend():
    # Logic to handle form submission goes here
    song_name = request.form.get('song')
    # Perform recommendation logic based on the submitted song name
    recommended_songs = ["Song 1", "Song 2", "Song 3"]  # Replace this with your recommendation logic
    return render_template('index.html', recommended_songs=recommended_songs)

# Route for rendering the homepage
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    # Start Kafka producer and consumer in background processes
    generate_recommendations()
    apply_recommendations()
    
    # Run the Flask application
    app.run(debug=True)
