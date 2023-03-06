# Generated by Django 4.1.2 on 2023-03-05 18:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fantapoma', '0013_alter_athlete_players_alter_player_franchs_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='athlete',
            name='is_user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='athlete',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='franchs',
            field=models.IntegerField(blank=True, default=450),
        ),
    ]
