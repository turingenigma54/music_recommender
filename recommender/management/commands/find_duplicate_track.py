from django.core.management.base import BaseCommand
from django.db.models import Count
from recommender.models import Track

class Command(BaseCommand):
    help = 'Find duplicate tracks in the database based on ID'

    def handle(self, *args, **options):
        # Find all IDs that have more than one track
        duplicate_ids = Track.objects.values('id').annotate(
            id_count=Count('id')
        ).filter(id_count__gt=1)

        if not duplicate_ids:
            self.stdout.write(self.style.SUCCESS('No duplicate IDs found.'))
            return

        self.stdout.write(self.style.WARNING(f'Found {len(duplicate_ids)} duplicate IDs:'))

        for dup in duplicate_ids:
            duplicate_tracks = Track.objects.filter(id=dup['id'])
            self.stdout.write(self.style.ERROR(f"\nDuplicate ID: {dup['id']}"))
            for track in duplicate_tracks:
                self.stdout.write(
                    f"  Track: {track.track_name}\n"
                    f"  Artist: {track.artists}\n"
                    f"  Album: {track.album_name}\n"
                    f"  Genre: {track.track_genre}\n"
                )

        self.stdout.write(self.style.WARNING(
            '\nPlease review these duplicates and decide which ones to keep. '
            'You may need to manually delete the unwanted duplicates or '
            'assign new IDs to them.'
        ))