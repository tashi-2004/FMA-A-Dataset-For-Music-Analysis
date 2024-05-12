import os
import json
import time
from kafka import KafkaProducer

# Kafka broker address
bootstrap_servers = 'localhost:9092'

# Create a Kafka producer
producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Kafka topic to publish music recommendations
topic = 'tashi'

# Path to the directory containing the dataset
dataset_path = '/home/laibu/Downloads/fma_large'

# Function to generate music recommendations for users
def generate_recommendations(directory):
    recommendations = []
    # Iterate through each directory in the dataset path
    for root, _, files in os.walk(directory):
        # Process only the first 5 files from each directory
        for file in files[:5]:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                recommendations.append({
                    'file_path': file_path,
                    'content': content.decode('latin1')  # Decode the content to string
                })
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
    return recommendations

# Generate music recommendations for each directory in the dataset path
for i in range(156):  # Assuming directories are named from 000 to 155
    directory = f"{i:03d}"  # Format the directory name with leading zeros
    directory_path = os.path.join(dataset_path, directory)
    # Check if the item in the dataset path is a directory
    if os.path.isdir(directory_path):
        # Generate music recommendations for the directory
        recommendations = generate_recommendations(directory_path)
        # Publish the recommendations to the Kafka topic
        for recommendation in recommendations:
            producer.send(topic, value=recommendation)
        # Sleep for a few seconds before processing the next directory
        time.sleep(1)

# Close the producer
producer.close()
