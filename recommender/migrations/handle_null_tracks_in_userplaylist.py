from django.db import migrations

def handle_null_tracks(apps, schema_editor):
    UserPlaylist = apps.get_model('recommender', 'UserPlaylist')
    UserPlaylist.objects.filter(track__isnull=True).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0006_alter_userplaylist_track'),  # Replace with the actual previous migration
    ]

    operations = [
        migrations.RunPython(handle_null_tracks),
    ]