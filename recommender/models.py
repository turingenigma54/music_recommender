from django.db import models
from django.conf import settings


class NewTrack(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    artists = models.TextField()
    duration_ms = models.IntegerField()
    release_date = models.CharField(max_length=20)  # Change this to CharField
    year = models.IntegerField()
    acousticness = models.FloatField()
    danceability = models.FloatField()
    energy = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    loudness = models.FloatField()
    speechiness = models.FloatField()
    tempo = models.FloatField()
    valence = models.FloatField()
    mode = models.IntegerField()
    key = models.IntegerField()
    popularity = models.IntegerField()
    explicit = models.BooleanField()

    class Meta:
        db_table = 'recommender_newtrack'

    def __str__(self):
        return f"{self.name} by {self.artists}"

class UserPlaylist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    playlist_name = models.CharField(max_length=255)
    track = models.ForeignKey(NewTrack, on_delete=models.CASCADE, to_field='id', null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'playlist_name', 'track')

    def __str__(self):
        return f"{self.user.username} - {self.playlist_name}"