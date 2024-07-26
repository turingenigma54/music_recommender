from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Track
from django.core.cache import cache
from django.db.models import Q, Count
from .utils import get_recommendations_from_db
from django.core.paginator import Paginator
import hashlib
@login_required
def dashboard(request):
    query = request.GET.get('query', '')
    search_type = request.GET.get('search_type', 'track')
    selected_genre = request.GET.get('genre', '')
    
    search_params = f"{query}_{search_type}_{selected_genre}"
    search_hash = hashlib.md5(search_params.encode()).hexdigest()
    
    tracks = cache.get(search_hash)
    if tracks is None:
        tracks = Track.objects.all()
        if query:
            if search_type == 'track':
                tracks = tracks.filter(track_name__icontains=query)
            elif search_type == 'artist':
                tracks = tracks.filter(artists__icontains=query)
        if selected_genre:
            tracks = tracks.filter(track_genre=selected_genre)
        tracks = list(tracks)
        
        cache.set(search_hash, tracks, 600)
    
    paginator = Paginator(tracks, 20)  # Show 20 tracks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unique genres, sorted alphabetically
    genres = list(Track.objects.values_list('track_genre', flat=True).distinct().order_by('track_genre'))
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'search_type': search_type,
        'selected_genre': selected_genre,
        'genres': genres,
    }
    
    return render(request, 'recommender/dashboard.html', context)
@login_required
def recommendations(request):
    track_id = request.GET.get('track_id')
    if not track_id:
        print("No track_id provided, redirecting to dashboard")
        return redirect('dashboard')

    print(f"Fetching track with ID: {track_id}")
    try:
        track = Track.objects.get(id=track_id)
        print(f"Found track: ID {track.id}, Name: {track.track_name}, Artists: {track.artists}")
    except Track.DoesNotExist:
        print(f"No track found with ID: {track_id}")
        return render(request, 'recommender/error.html', {'message': 'Track not found'})
    except ValueError:
        print(f"Invalid track ID provided: {track_id}")
        return render(request, 'recommender/error.html', {'message': 'Invalid track ID'})

    print("Getting recommendations...")
    recommended_tracks = get_recommendations_from_db(track.track_name, track.artists, n=20)

    print(f"Rendering template with {len(recommended_tracks)} recommendations")
    return render(request, 'recommender/recommendations.html', {
        'selected_track': track,
        'recommended_tracks': recommended_tracks,
        'num_recommendations': len(recommended_tracks)
    })