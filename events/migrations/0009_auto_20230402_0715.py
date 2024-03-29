# Generated by Django 4.1.2 on 2023-04-02 05:15

from django.db import migrations
import uuid


def gen_uuid(apps, schema_editor):
    events = apps.get_model('events', 'Event')
    for row in events.objects.all():
        row.uuid = uuid.uuid4()
        row.save(update_fields=['url'])


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_event_url'),
    ]

    operations = [
        # omit reverse_code=... if you don't want the migration to be reversible.
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
    ]
