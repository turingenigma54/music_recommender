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
    all_tracks = Track.objects.all().values('id', 'track_name', 'artists', *features)
    
    # Convert to a list of dictionaries
    tracks_list = list(all_tracks)

    # Extract features for similarity calculation
    feature_matrix = np.array([[track[f] for f in features] for track in tracks_list])

    # Normalize features
    scaler = MinMaxScaler()
    normalized_features = scaler.fit_transform(feature_matrix)

    # Calculate similarity
    track_index = next(i for i, t in enumerate(tracks_list) if t['track_name'] == track_name)
    track_features = normalized_features[track_index].reshape(1, -1)
    similarities = cosine_similarity(track_features, normalized_features)[0]

    # Get indices of top N similar tracks
    similar_indices = similarities.argsort()[::-1][1:n+1]

    # Get the similar tracks
    recommendations = [tracks_list[i] for i in similar_indices]

    return recommendations