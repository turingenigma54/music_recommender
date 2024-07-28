import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from .models import Track
import random

class ImprovedRecommender:
    def __init__(self):
        self.tracks = None
        self.feature_matrix = None
        self.scaler = MinMaxScaler()

    def fit(self):
        self._prepare_content_based()

    def _prepare_content_based(self):
        features = ['popularity', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                    'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
        
        self.tracks = list(Track.objects.all().values('id', 'track_name', 'artists', 'track_genre', *features))
        
        feature_matrix = np.array([[track[f] for f in features] for track in self.tracks])
        self.feature_matrix = self.scaler.fit_transform(feature_matrix)

    def get_recommendations(self, track_id, n=20):
        track_index = next(i for i, t in enumerate(self.tracks) if t['id'] == track_id)
        track_features = self.feature_matrix[track_index].reshape(1, -1)

        # Compute similarities in batches
        batch_size = 1000
        num_tracks = len(self.tracks)
        all_similarities = []

        for i in range(0, num_tracks, batch_size):
            batch = self.feature_matrix[i:i+batch_size]
            similarities = cosine_similarity(track_features, batch)[0]
            all_similarities.extend(similarities)

        # Get top N recommendations
        top_indices = np.argsort(all_similarities)[::-1][1:n+1]  # Exclude the input track
        recommendations = [self.tracks[i] for i in top_indices]

        return recommendations

def get_recommendations_from_db(track_name, artists, n=20):
    recommender = ImprovedRecommender()
    recommender.fit()

    try:
        track = Track.objects.get(track_name=track_name, artists__icontains=artists.split(';')[0])
    except Track.DoesNotExist:
        print("No matching track found.")
        return []
    except Track.MultipleObjectsReturned:
        print("Multiple tracks found. Using the first one.")
        track = Track.objects.filter(track_name=track_name, artists__icontains=artists.split(';')[0]).first()

    recommendations = recommender.get_recommendations(track.id, n)
    return recommendations