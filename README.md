# FMA-A-Dataset-For-Music-Analysis

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

## Data

All metadata and features for all tracks are distributed in **[`fma_metadata.zip`]** (342 MiB).
The below tables can be used with [pandas] or any other data analysis tool.
See the [paper] or the [`usage.ipynb`] notebook for a description.
* `tracks.csv`: per track metadata such as ID, title, artist, genres, tags and play counts, for all 106,574 tracks.
* `genres.csv`: all 163 genres with name and parent (used to infer the genre hierarchy and top-level genres).
* `features.csv`: common features extracted with [librosa].
* `echonest.csv`: audio features provided by [Echonest] (now [Spotify]) for a subset of 13,129 tracks.

[pandas]:   https://pandas.pydata.org/
[librosa]:  https://librosa.org/
[spotify]:  https://www.spotify.com/
[echonest]: https://web.archive.org/web/20170519050040/http://the.echonest.com/

Then, you got various sizes of MP3-encoded audio data:

1. **[`fma_small.zip`]**: 8,000 tracks of 30s, 8 balanced genres (GTZAN-like) (7.2 GiB)
2. **[`fma_medium.zip`]**: 25,000 tracks of 30s, 16 unbalanced genres (22 GiB)
3. **[`fma_large.zip`]**: 106,574 tracks of 30s, 161 unbalanced genres (93 GiB)
4. **[`fma_full.zip`]**: 106,574 untrimmed tracks, 161 unbalanced genres (879 GiB)

[`fma_metadata.zip`]: https://os.unil.cloud.switch.ch/fma/fma_metadata.zip
[`fma_small.zip`]:    https://os.unil.cloud.switch.ch/fma/fma_small.zip
[`fma_medium.zip`]:   https://os.unil.cloud.switch.ch/fma/fma_medium.zip
[`fma_large.zip`]:    https://os.unil.cloud.switch.ch/fma/fma_large.zip
[`fma_full.zip`]:     https://os.unil.cloud.switch.ch/fma/fma_full.zip
## Setup
1. **Clone the Repository**: Clone or download the repository to your local machine.
    ```bash
    git clone <https://github.com/tashi-2004/FMA-A-Dataset-For-Music-Analysis>
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

## Notes (Apache Spark)
![1](https://github.com/user-attachments/assets/362d6402-08ca-4427-a0a0-4423b36fb932)
![2](https://github.com/user-attachments/assets/cc842da4-407d-4c78-9a34-78a232f9ed0e)
![3](https://github.com/user-attachments/assets/74af1825-6cef-47b6-8763-81c8e2e242de)
![4](https://github.com/user-attachments/assets/a78a997c-2608-4b12-857f-8f4017b81252)
![5](https://github.com/user-attachments/assets/692c8a4d-6c99-4aae-ab7f-63c7444bc68d)

## Customization
You can customize the scripts according to your requirements, such as adjusting feature extraction parameters, changing MongoDB or Kafka configurations, or modifying recommendation model algorithms.

## Contributors
- Tashfeen Abbasi
- [Laiba Mazhar](https://github.com/laiba-mazhar)
- [Rafia Khan](https://github.com/rakhan2)

Feel free to contribute to this project by submitting issues or pull requests. Enjoy analyzing and recommending music with this comprehensive toolkit!
