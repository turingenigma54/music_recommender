from django.db import models
from django.conf import settings
# Create your models here.
class Track(models.Model):
    track_id = models.CharField(max_length=255, unique=True)
    artists = models.TextField()
    album_name = models.TextField()
    track_name = models.TextField()
    popularity = models.IntegerField()
    duration_ms = models.IntegerField()
    explicit = models.BooleanField()
    danceability = models.FloatField()
    energy = models.FloatField()
    key = models.IntegerField()
    loudness = models.FloatField()
    mode = models.IntegerField()
    speechiness = models.FloatField()
    acousticness = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    valence = models.FloatField()
    tempo = models.FloatField()
    time_signature = models.IntegerField()
    track_genre = models.CharField(max_length=255)

class UserPlaylist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    playlist_name = models.CharField(max_length=255)
    track = models.ForeignKey('Track', on_delete=models.CASCADE, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'playlist_name', 'track')

    def __str__(self):
        return f"{self.user.username} - {self.playlist_name}"