from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('recommendations/', views.recommendations, name='recommendations'),
    path('playlists/', views.user_playlists, name='user_playlists'),
    path('playlists/<str:playlist_name>/', views.playlist_detail, name='playlist_detail'),
    path('add-to-playlist/<str:track_id>/', views.add_to_playlist, name='add_to_playlist'),
    path('remove-from-playlist/<str:playlist_name>/<int:track_id>/', views.remove_from_playlist, name='remove_from_playlist'),
]