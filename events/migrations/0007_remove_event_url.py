# Generated by Django 4.1.2 on 2023-04-02 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_alter_event_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='url',
        ),
    ]