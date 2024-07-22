import os 
import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from django.conf import settings

def load_and_preprocess_data():
    file_path = os.path.join(settings.BASE_DIR, 'data_set', 'dataset.csv')
    df = pd.read_csv(file_path)

    features = ['popularity', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 
                'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
    scaler = MinMaxScaler()
    df[features] = scaler.fit_transform(df[features])
    return df

def get_recommendations_from_file(track_name, df, n =5) :

    track = df[df['track_name'] == track_name]
    if track.empty:
        return []
    track = track.iloc[0]
    features = ['popularity', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 
                'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
    similarity = cosine_similarity(track[features], df[features])[0]

    similar_indices = similarity.argsort()[::-1][1:n+1]
    recommendations = df.iloc[similar_indices][['track_name', 'artist_name', 'album_name']]
    return recommendations.to_dict('records')
df = load_and_preprocess_data()
    