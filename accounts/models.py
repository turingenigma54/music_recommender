from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    spotify_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    spotify_access_token = models.CharField(max_length=255, null=True, blank=True)
    spotify_refresh_token = models.CharField(max_length=255, null=True, blank=True)
    

    def __str__(self):
        return self.username
    
