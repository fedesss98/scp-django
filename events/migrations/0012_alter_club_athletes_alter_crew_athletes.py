# Generated by Django 4.1.2 on 2023-04-16 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_alter_club_athletes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='athletes',
            field=models.ManyToManyField(blank=True, to='events.athlete'),
        ),
        migrations.AlterField(
            model_name='crew',
            name='athletes',
            field=models.ManyToManyField(to='events.athlete'),
        ),
    ]
