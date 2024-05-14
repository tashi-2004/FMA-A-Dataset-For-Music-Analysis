# BDA-PROJECT-FMA-A-Dataset-For-Music-Analysis

This repository contains scripts for analyzing music features, training recommendation models, and building a real-time recommendation system using Apache Kafka.

## Features

- **load1.py**: Extracts audio features using Librosa and prints them for each audio file. Also includes plotting of normalized MFCCs, Spectral Centroid, and Zero-Crossing Rate.
- **mongodb1.py**: Inserts audio features into MongoDB for storage and retrieval.
- **connector.py**: Connects Apache Spark with MongoDB to read data into Spark DataFrames.
- **PHASE2.py**: Trains a music recommendation model using Annoy and performs nearest neighbor search.
- **producer.py**: Streams music features to Kafka for real-time processing.
- **consumer.py**: Consumes music recommendations from Kafka and applies them.

## Setup

1. **Clone the Repository**: Clone or download the repository to your local machine.
2. **Install Dependencies**: Install the required Python dependencies using `pip install -r requirements.txt`.
3. **Set Up MongoDB**: Make sure MongoDB is installed and running on your system. Update MongoDB connection strings in relevant scripts.
4. **Set Up Kafka**: Install and run Apache Kafka on your system. Update Kafka broker address in `producer.py` and `consumer.py`.
5. **Run Scripts**: Execute the scripts in the following order:


## Usage

- Use `load1.py` to extract and visualize audio features.
- Use `mongodb1.py` to store audio features in MongoDB.
- Use `connector.py` to connect Spark with MongoDB for data analysis.
- Use `PHASE2.py` to train recommendation models and perform nearest neighbor search.
- Use `producer.py` to stream music features to Kafka.
- Use `consumer.py` to consume music recommendations from Kafka and apply them.

## Customization

You can customize the scripts according to your requirements, such as adjusting feature extraction parameters, changing MongoDB or Kafka configurations, or modifying recommendation model algorithms.

## Contributors

- Tashfeen Abbasi
- Laiba Mazhar
- Rafia Khan
