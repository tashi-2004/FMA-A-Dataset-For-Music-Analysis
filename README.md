# BDA-PROJECT-FMA-A-Dataset-For-Music-Analysis

## Overview
This repository contains scripts for analyzing music features, training recommendation models, and building a real-time recommendation system using Apache Kafka.

## Features
- **load1.py**: Extracts audio features using Librosa and prints them for each audio file. Also includes plotting of normalized MFCCs, Spectral Centroid, and Zero-Crossing Rate.
- **mongodb1.py**: Inserts audio features into MongoDB for storage and retrieval.
- **connector.py**: Connects Apache Spark with MongoDB to read data into Spark DataFrames.
- **PHASE2.py**: Trains a music recommendation model using Annoy and performs nearest neighbor search.
- **producer.py**: Streams music features to Kafka for real-time processing.
- **consumer.py**: Consumes music recommendations from Kafka and applies them.
- **app.py**: A web application to upload audio files and get insights.
- **index.html**: A simple web interface for uploading files and displaying insights.

## Setup
1. **Clone the Repository**: Clone or download the repository to your local machine.
    ```bash
    git clone <https://github.com/tashi-2004/BDA-PROJECT-FMA-A-Dataset-For-Music-Analysis>
    ```
2. **Install Dependencies**: Install the required Python dependencies using:
    ```bash
    pip install -r requirements.txt
    ```
3. **Set Up MongoDB**: Ensure MongoDB is installed and running on your system. Update MongoDB connection strings in the relevant scripts.
4. **Set Up Kafka**: Install and run Apache Kafka on your system. Update the Kafka broker address in `producer.py` and `consumer.py`.
5. **Run Scripts**: Execute the scripts in the following order:
    - **Extract and Visualize Audio Features**: Run `load1.py` to extract and visualize audio features from your audio files.
    - **Store Audio Features in MongoDB**: Run `mongodb1.py` to store the extracted audio features in MongoDB.
    - **Data Analysis with Spark**: Run `connector.py` to connect Spark with MongoDB and perform data analysis using Spark DataFrames.
    - **Train Recommendation Models**: Run `PHASE2.py` to train music recommendation models using Annoy and perform nearest neighbor searches.
    - **Stream Music Features to Kafka**: Run `producer.py` to stream music features to Kafka for real-time processing.
    - **Consume Music Recommendations from Kafka**: Run `consumer.py` to consume music recommendations from Kafka and apply them.
    - **Web Interface for Audio Files**: Use `app.py` and `index.html` to upload audio files via a web interface and get insights.

## Usage
1. **Extract and Visualize Audio Features**: Run `load1.py` to extract and visualize audio features from your audio files.
2. **Store Audio Features in MongoDB**: Run `mongodb1.py` to store the extracted audio features in MongoDB.
3. **Data Analysis with Spark**: Run `connector.py` to connect Spark with MongoDB and perform data analysis using Spark DataFrames.
4. **Train Recommendation Models**: Run `PHASE2.py` to train music recommendation models using Annoy and perform nearest neighbor searches.
5. **Stream Music Features to Kafka**: Run `producer.py` to stream music features to Kafka for real-time processing.
6. **Consume Music Recommendations from Kafka**: Run `consumer.py` to consume music recommendations from Kafka and apply them.
7. **Web Interface for Audio Files**: Use `app.py` and `index.html` to upload audio files via a web interface and get insights.

## Customization
You can customize the scripts according to your requirements, such as adjusting feature extraction parameters, changing MongoDB or Kafka configurations, or modifying recommendation model algorithms.

## Contributors
- Tashfeen Abbasi
- Laiba Mazhar
- Rafia Khan

Feel free to contribute to this project by submitting issues or pull requests. Enjoy analyzing and recommending music with this comprehensive toolkit!
