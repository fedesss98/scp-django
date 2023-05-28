# Generated by Django 4.1.2 on 2023-04-02 05:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_remove_event_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='url',
            field=models.CharField(default=uuid.uuid4, max_length=200, null=True),
        ),
    ]
