from django.db import models

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
    
    def __str__(self):
        return self.track_name
