from .models import Track
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_recommendations_from_db(track_name, n=20):
    try:
        track = Track.objects.get(track_name=track_name)
    except Track.DoesNotExist:
        return []

    features = ['popularity', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 
                'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']

    # Get all tracks and their features
    all_tracks = Track.objects.exclude(id=track.id).values('id', 'track_name', 'artists', 'track_genre', *features)
    
    # Convert to a list of dictionaries
    tracks_list = list(all_tracks)

    # Extract features for similarity calculation
    feature_matrix = np.array([[t[f] for f in features] for t in tracks_list])

    # Normalize features
    scaler = MinMaxScaler()
    normalized_features = scaler.fit_transform(feature_matrix)

    # Calculate similarity
    track_features = np.array([getattr(track, f) for f in features]).reshape(1, -1)
    track_features_normalized = scaler.transform(track_features)
    similarities = cosine_similarity(track_features_normalized, normalized_features)[0]

    # Get indices of top N similar tracks
    similar_indices = similarities.argsort()[::-1][:n]

    # Get the similar tracks
    recommendations = [tracks_list[i] for i in similar_indices]

    return recommendations