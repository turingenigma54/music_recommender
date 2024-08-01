import csv
from django.core.management.base import BaseCommand
from recommender.models import Track
from django.db import IntegrityError, transaction

class Command(BaseCommand):
    help = 'Import tracks from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            total_rows = sum(1 for row in csv_reader)
            file.seek(0)
            next(csv_reader)  # Skip header row
            
            for i, row in enumerate(csv_reader, 1):
                try:
                    with transaction.atomic():
                        Track.objects.update_or_create(
                            track_id=row['track_id'],
                            defaults={
                                'artists': row['artists'],
                                'album_name': row['album_name'],
                                'name': row['name'],
                                'popularity': int(row['popularity']),
                                'duration_ms': int(row['duration_ms']),
                                'explicit': row['explicit'].lower() == 'true',
                                'danceability': float(row['danceability']),
                                'energy': float(row['energy']),
                                'key': int(row['key']),
                                'loudness': float(row['loudness']),
                                'mode': int(row['mode']),
                                'speechiness': float(row['speechiness']),
                                'acousticness': float(row['acousticness']),
                                'instrumentalness': float(row['instrumentalness']),
                                'liveness': float(row['liveness']),
                                'valence': float(row['valence']),
                                'tempo': float(row['tempo']),
                                'time_signature': int(row['time_signature']),
                                'track_genre': row['track_genre']
                            }
                        )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error importing track {row['track_id']}: {str(e)}"))
                
                if i % 1000 == 0:
                    self.stdout.write(self.style.SUCCESS(f"Imported {i}/{total_rows} tracks"))

        self.stdout.write(self.style.SUCCESS('Successfully imported all tracks'))