import os
import librosa
import numpy as np
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Update connection string as needed
db = client['project']
collection = db['tashi']

# Path to the folder containing all the folders with audio files
root_folder = '/home/laibu/Downloads/fma_large'

# Initialize lists to store features for all audio files
all_mfccs = []
all_centroids = []
all_zero_crossing_rates = []

# Define a fixed length for MFCC arrays
max_frames = 500

# Number of files to process per folder
files_per_folder = 5

# Loop through each subfolder (000, 001, ..., 155)
for folder_name in sorted(os.listdir(root_folder)):  # Iterate over all folders
    folder_path = os.path.join(root_folder, folder_name)
    files_processed = 0  # Keep track of the number of files processed

    # Skip if it's not a directory
    if not os.path.isdir(folder_path):
        continue

    # Loop through each audio file in the current subfolder
    for audio_file in os.listdir(folder_path):
        if audio_file.endswith('.mp3'):
            audio_path = os.path.join(folder_path, audio_file)

            # Load audio file
            y, sr = librosa.load(audio_path)

            # Extract MFCCs
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

            # Pad or truncate MFCCs to ensure fixed length
            if mfccs.shape[1] < max_frames:
                # Pad with zeros
                mfccs = np.pad(mfccs, ((0, 0), (0, max_frames - mfccs.shape[1])), mode='constant')
            elif mfccs.shape[1] > max_frames:
                # Truncate
                mfccs = mfccs[:, :max_frames]

            # Calculate spectral centroid
            centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
            centroid = centroid[:, :max_frames]  # Truncate to match MFCCs length
            centroid_mean = np.mean(centroid)  # Calculate the mean value of the centroid
            centroid = np.full_like(mfccs, centroid_mean)  # Create an array with the same shape as MFCCs, filled with the centroid mean

            # Calculate zero-crossing rate
            zero_crossing_rate = librosa.feature.zero_crossing_rate(y)
            zero_crossing_rate = zero_crossing_rate[:, :max_frames]  # Truncate to match MFCCs length
            zero_crossing_rate_mean = np.mean(zero_crossing_rate)  # Calculate the mean value of the zero-crossing rate
            zero_crossing_rate = np.full_like(mfccs, zero_crossing_rate_mean)  # Create an array with the same shape as MFCCs, filled with the zero-crossing rate mean

            # Append MFCCs, spectral centroid, and zero-crossing rate to the lists
            all_mfccs.append(mfccs)
            all_centroids.append(centroid)
            all_zero_crossing_rates.append(zero_crossing_rate)

            files_processed += 1

            # Prepare document to insert into MongoDB
            document = {
                "folder": folder_name,
                "audio_file": audio_file,
                "mfccs": mfccs.tolist(),
                "spectral_centroid": centroid.tolist(),
                "zero_crossing_rate": zero_crossing_rate.tolist()
            }

            # Insert document into MongoDB collection
            collection.insert_one(document)

            # Break if processed the required number of files per folder
            if files_processed >= files_per_folder:
                break

# Convert the lists of features to numpy arrays
all_mfccs = np.array(all_mfccs)
all_centroids = np.array(all_centroids)
all_zero_crossing_rates = np.array(all_zero_crossing_rates)

# Get the number of frames (columns) in the MFCCs array
num_frames = all_mfccs.shape[2]
