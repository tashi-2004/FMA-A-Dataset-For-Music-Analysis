import os
import json
import time
import librosa
import random
from kafka import KafkaProducer

# Kafka broker address
bootstrap_servers = 'localhost:9092'

# Create a Kafka producer
producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                         value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'))

# Kafka topic to publish music recommendations
topic = 'tashi'

# Path to the directory containing the dataset
dataset_path = '/home/laibu/Downloads/fma_large'

# Function to extract audio features
def extract_features(audio_file):
    try:
        # Load audio file and extract features using Librosa
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

# Generate music recommendations for each directory from "000" to "155"
for i in range(156):
    directory = f"{i:03d}"  # Format the directory name with leading zeros
    directory_path = os.path.join(dataset_path, directory)
    # Check if the directory exists
    if os.path.isdir(directory_path):
        # Print the directory being processed
        print(f"Processing directory: {directory_path}")
        # Get a list of all audio files in the directory
        audio_files = [f for f in os.listdir(directory_path) if f.endswith('.mp3')]
        # Randomly select 5 songs from the list
        selected_files = random.sample(audio_files, min(5, len(audio_files)))
        # Process each selected audio file
        for file_name in selected_files:
            file_path = os.path.join(directory_path, file_name)
            # Extract features from the audio file
            features = extract_features(file_path)
            if features:
                # Publish the features to the Kafka topic
                producer.send(topic, value=features)
        # Sleep for a few seconds before processing the next directory
        time.sleep(1)

# Close the producer
producer.close()

