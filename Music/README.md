# Music Recommendation System using KNN

This project implements a music recommendation system using K-Nearest Neighbors (KNN) algorithm. The system analyzes audio features of songs and recommends similar tracks based on their musical characteristics.

## Features

- Audio feature extraction using librosa
- KNN-based similarity matching
- Song recommendation based on audio features
- Support for various audio formats (mp3, wav)

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Place your music files in the `Data` directory

3. Run the recommendation system:
```bash
python recommender.py
```

## Usage

The system will:
1. Extract audio features from your music collection
2. Build a KNN model based on these features
3. Allow you to get recommendations for any song in your collection

## Requirements

- Python 3.8+
- Dependencies listed in requirements.txt
