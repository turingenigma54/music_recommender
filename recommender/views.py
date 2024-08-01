from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Track , UserPlaylist
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
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserPlaylist

@login_required
def user_playlists(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            playlist_name = request.POST.get('playlist_name')
            if playlist_name and playlist_name.strip():
                # Create the playlist, but don't associate it with any track yet
                UserPlaylist.objects.create(user=request.user, playlist_name=playlist_name.strip())
        elif action == 'delete':
            playlist_name = request.POST.get('playlist_name')
            if playlist_name:
                UserPlaylist.objects.filter(user=request.user, playlist_name=playlist_name).delete()

    # Fetch playlists and their track counts
    playlists = UserPlaylist.objects.filter(user=request.user)\
                .values('playlist_name')\
                .annotate(track_count=Count('track', distinct=True))\
                .order_by('playlist_name')
    
    return render(request, 'recommender/user_playlists.html', {'playlists': playlists})
@login_required
def playlist_detail(request, playlist_name):
    playlist_tracks = UserPlaylist.objects.filter(
        user=request.user, 
        playlist_name=playlist_name, 
        track__isnull=False
    ).select_related('track')
    
    if request.method == 'POST':
        track_id = request.POST.get('track_id')
        if track_id:
            UserPlaylist.objects.filter(user=request.user, playlist_name=playlist_name, track_id=track_id).delete()
            return redirect('playlist_detail', playlist_name=playlist_name)

    context = {
        'playlist_name': playlist_name,
        'tracks': [item.track for item in playlist_tracks],
    }
    return render(request, 'recommender/playlist_detail.html', context)

@login_required
def add_to_playlist(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    user_playlists = UserPlaylist.objects.filter(user=request.user).values('playlist_name').annotate(
        track_count=Count('track')
    ).distinct().order_by('playlist_name')

    if request.method == 'POST':
        playlist_names = request.POST.getlist('existing_playlists')
        new_playlist_name = request.POST.get('new_playlist_name')
        
        for playlist_name in playlist_names:
            if playlist_name.strip():  # Check if playlist_name is not empty after stripping whitespace
                UserPlaylist.objects.get_or_create(
                    user=request.user,
                    playlist_name=playlist_name.strip(),
                    track=track
                )

        if new_playlist_name and new_playlist_name.strip():  # Check if new_playlist_name is not empty after stripping whitespace
            UserPlaylist.objects.create(
                user=request.user,
                playlist_name=new_playlist_name.strip(),
                track=track
            )

        return redirect('user_playlists')

    context = {
        'track': track,
        'user_playlists': user_playlists
    }

    return render(request, 'recommender/add_to_playlist.html', context)
@login_required
def remove_from_playlist(request, playlist_name, track_id):
    UserPlaylist.objects.filter(user=request.user, playlist_name=playlist_name, track_id=track_id).delete()
    return redirect('playlist_detail', playlist_name=playlist_name)