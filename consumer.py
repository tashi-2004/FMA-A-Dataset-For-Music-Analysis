import json
from kafka import KafkaConsumer

# Kafka broker address
bootstrap_servers = 'localhost:9092'

# Kafka topic to consume music recommendations
topic = 'tashi'

# Create a Kafka consumer
consumer = KafkaConsumer(topic,
                         bootstrap_servers=bootstrap_servers,
                         value_deserializer=lambda v: json.loads(v.decode('utf-8')))

# Function to apply recommendations based on features
def apply_recommendations(features):
    # Here you can implement the logic to apply recommendations based on the features received
    # For demonstration, let's just print the features
    print("Received features:", features)

# Continuously consume messages and apply recommendations
for message in consumer:
    # Get the features from the message value
    features = message.value
    # Apply recommendations based on the features
    apply_recommendations(features)

