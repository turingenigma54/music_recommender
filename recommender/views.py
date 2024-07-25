from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Track
from django.db.models import Q
from .utils import get_recommendations_from_db
from django.core.paginator import Paginator

@login_required
def dashboard(request):
    query = request.GET.get('query', '')
    tracks = Track.objects.all()
    
    if query:
        tracks = tracks.filter(
            Q(track_name__icontains=query) | 
            Q(artists__icontains=query) |
            Q(track_genre__icontains=query)
        )
    
    paginator = Paginator(tracks, 20)  # Show 20 tracks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'recommender/dashboard.html', {'page_obj': page_obj, 'query': query})

@login_required
def recommendations(request):
    track_id = request.GET.get('track_id')
    if not track_id:
        return redirect('dashboard')
    
    try:
        track = Track.objects.filter(id=track_id).first()
        if not track:
            return render(request, 'recommender/error.html', {'message': 'Track not found'})
    except ValueError:
        return render(request, 'recommender/error.html', {'message': 'Invalid track ID'})
    
    recommended_tracks = get_recommendations_from_db(track.track_name, n=20)
    
    return render(request, 'recommender/recommendations.html', {
        'selected_track': track,
        'recommended_tracks': recommended_tracks,
        'num_recommendations': len(recommended_tracks)
    })