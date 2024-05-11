import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Path to the folder containing all the folders with audio files.
root_folder = '/home/laibu/Downloads/fma_large'

# Initialize lists to store features for all audio files
all_mfccs = []
all_centroids = []
all_zero_crossing_rates = []

# Define a fixed length for MFCC arrays
max_frames = 500

# Loop through each subfolder (000, 001, ..., 155)
for folder_index in range(156):  # Iterate over all folders
    folder_name = '{:03d}'.format(folder_index)  # Format folder index with leading zeros
    folder_path = os.path.join(root_folder, folder_name)
    
    # Check if the folder exists
    if os.path.isdir(folder_path):
        # List all files in the folder
        files = os.listdir(folder_path)
        # Filter out only .mp3 files
        audio_files = [file for file in files if file.endswith('.mp3')]
        
        # Check if there are any audio files in the folder
        if audio_files:
            # Select the first audio file
            audio_file = audio_files[0]
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

            # Calculate zero-crossing rate
            zero_crossing_rate = librosa.feature.zero_crossing_rate(y)
            zero_crossing_rate = zero_crossing_rate[:, :max_frames]  # Truncate to match MFCCs length

            # Normalize features
            min_max_scaler = MinMaxScaler()
            mfccs_normalized = min_max_scaler.fit_transform(mfccs.T).T
            centroid_normalized = min_max_scaler.fit_transform(centroid.T).T
            zero_crossing_rate_normalized = min_max_scaler.fit_transform(zero_crossing_rate.T).T

            # Append normalized MFCCs, spectral centroid, and zero-crossing rate to the lists
            all_mfccs.append(mfccs_normalized)
            all_centroids.append(centroid_normalized)
            all_zero_crossing_rates.append(zero_crossing_rate_normalized)

            # Print features for the current audio file
            print(f"Features for {audio_file} in folder {folder_name}:")
            print("Normalized MFCCs:")
            print(mfccs_normalized[:10])  # Print the first 10 rows
            print("\nNormalized Spectral Centroid:")
            print(centroid_normalized)
            print("\nNormalized Zero-Crossing Rate:")
            print(zero_crossing_rate_normalized)
            print("-----------------------------------------------------------------------------------------------------------------------------")
            print("\n\n")

# Convert the lists of features to numpy arrays
all_mfccs = np.array(all_mfccs)
all_centroids = np.array(all_centroids)
all_zero_crossing_rates = np.array(all_zero_crossing_rates)

# Get the number of frames (columns) in the MFCCs array
num_frames = all_mfccs.shape[2]

# Plot MFCCs for the first audio file using scatter plot
plt.figure(figsize=(12,7))
plt.scatter(range(num_frames), all_mfccs[0, 0, :], s=10, marker='o', color='blue')
plt.title('Normalized MFCCs for Spotify Audios')
plt.xlabel('Frame Index')
plt.ylabel('MFCC Value')
plt.grid(True)  # Add grid lines
plt.tight_layout()
plt.show()

# Plot normalized spectral centroid for the first audio file
plt.figure(figsize=(12, 7))
plt.plot(range(num_frames), all_centroids[0, 0, :], color='red')
plt.title('Normalized Spectral Centroid for Spotify Audios')
plt.xlabel('Frame Index')
plt.ylabel('Spectral Centroid')
plt.grid(True)  # Add grid lines
plt.tight_layout()
plt.show()

# Plot normalized zero-crossing rate for the first audio file
plt.figure(figsize=(12, 7))
plt.plot(range(num_frames), all_zero_crossing_rates[0, 0, :], color='green')
plt.title('Normalized Zero-Crossing Rate for Spotify Audios')
plt.xlabel('Frame Index')
plt.ylabel('Zero-Crossing Rate')
plt.grid(True)  # Add grid lines
plt.tight_layout()
plt.show()

