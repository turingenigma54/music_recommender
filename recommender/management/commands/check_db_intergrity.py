from django.core.management.base import BaseCommand
from django.db.models import Count
from recommender.models import Track

class Command(BaseCommand):
    help = 'Check database integrity for Track model'

    def handle(self, *args, **options):
        # Check for duplicate IDs
        duplicate_ids = Track.objects.values('id').annotate(
            id_count=Count('id')
        ).filter(id_count__gt=1)

        if duplicate_ids:
            self.stdout.write(self.style.ERROR(f'Found {len(duplicate_ids)} duplicate IDs:'))
            for dup in duplicate_ids:
                tracks = Track.objects.filter(id=dup['id'])
                self.stdout.write(self.style.WARNING(f"ID {dup['id']} appears {dup['id_count']} times:"))
                for track in tracks:
                    self.stdout.write(f"  {track.track_name} by {track.artists} (Track ID: {track.track_id})")
        else:
            self.stdout.write(self.style.SUCCESS('No duplicate IDs found.'))

        # Check for duplicate track_ids
        duplicate_track_ids = Track.objects.values('track_id').annotate(
            track_id_count=Count('track_id')
        ).filter(track_id_count__gt=1)

        if duplicate_track_ids:
            self.stdout.write(self.style.ERROR(f'Found {len(duplicate_track_ids)} duplicate track_ids:'))
            for dup in duplicate_track_ids:
                tracks = Track.objects.filter(track_id=dup['track_id'])
                self.stdout.write(self.style.WARNING(f"Track ID {dup['track_id']} appears {dup['track_id_count']} times:"))
                for track in tracks:
                    self.stdout.write(f"  ID: {track.id}, {track.track_name} by {track.artists}")
        else:
            self.stdout.write(self.style.SUCCESS('No duplicate track_ids found.'))