import csv
from django.core.management.base import BaseCommand
from recommender.models import NewTrack
from django.db import transaction

class Command(BaseCommand):
    help = 'Import tracks from new CSV file into NewTrack table'

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
                        NewTrack.objects.create(
                            id=row['id'],
                            name=row['name'],
                            artists=row['artists'],
                            duration_ms=int(row['duration_ms']),
                            release_date=row['release_date'],  # Store as string
                            year=int(row['year']),
                            acousticness=float(row['acousticness']),
                            danceability=float(row['danceability']),
                            energy=float(row['energy']),
                            instrumentalness=float(row['instrumentalness']),
                            liveness=float(row['liveness']),
                            loudness=float(row['loudness']),
                            speechiness=float(row['speechiness']),
                            tempo=float(row['tempo']),
                            valence=float(row['valence']),
                            mode=int(row['mode']),
                            key=int(row['key']),
                            popularity=int(row['popularity']),
                            explicit=row['explicit'].lower() == 'true'
                        )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error importing track {row['id']}: {str(e)}"))

                if i % 1000 == 0:
                    self.stdout.write(self.style.SUCCESS(f"Imported {i}/{total_rows} tracks"))

        self.stdout.write(self.style.SUCCESS('Successfully imported all tracks'))