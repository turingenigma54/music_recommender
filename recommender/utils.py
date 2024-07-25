from .models import Track
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_recommendations_from_db(track_name, artists, n=20):
    print(f"Searching for track: '{track_name}' by {artists}")
    
    try:
        # Split artists string into a list
        artist_list = [artist.strip() for artist in artists.split(';')]
        
        # Filter tracks by name and check if any of the artists match
        tracks = Track.objects.filter(track_name=track_name).filter(artists__icontains=artist_list[0])
        
        print(f"Found {tracks.count()} tracks matching '{track_name}' and artist '{artist_list[0]}':")
        for t in tracks:
            print(f"  ID: {t.id}, Name: {t.track_name}, Artists: {t.artists}")
        
        if tracks.count() > 1:
            print("Warning: Multiple tracks found with the same name and artist. Using the first one.")
        
        track = tracks.first()
        if not track:
            print("No matching track found.")
            return []
    except Exception as e:
        print(f"Error finding track: {str(e)}")
        return []

    print(f"Using track: ID {track.id}, Name: {track.track_name}, Artists: {track.artists}")


    features = ['popularity', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']

    print("Fetching all other tracks...")
    all_tracks = Track.objects.exclude(id=track.id).values('id', 'track_name', 'artists', 'track_genre', *features)
    print(f"Fetched {all_tracks.count()} tracks for comparison")

    tracks_list = list(all_tracks)

    print("Extracting and normalizing features...")
    feature_matrix = np.array([[t[f] for f in features] for t in tracks_list])
    scaler = MinMaxScaler()
    normalized_features = scaler.fit_transform(feature_matrix)

    print("Calculating similarities...")
    track_features = np.array([getattr(track, f) for f in features]).reshape(1, -1)
    track_features_normalized = scaler.transform(track_features)
    similarities = cosine_similarity(track_features_normalized, normalized_features)[0]

    print("Finding most similar tracks...")
    similar_indices = similarities.argsort()[::-1][:n]

    recommendations = [tracks_list[i] for i in similar_indices]
    print(f"Found {len(recommendations)} recommendations")

    return recommendations