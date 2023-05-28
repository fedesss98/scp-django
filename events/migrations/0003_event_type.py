# Generated by Django 4.1.2 on 2023-03-31 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_location_event_url_alter_event_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='type',
            field=models.CharField(choices=[('REG', 'Regional'), ('NAT', 'National')], default='REG', max_length=80),
        ),
    ]
