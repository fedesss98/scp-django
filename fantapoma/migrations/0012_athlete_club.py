# Generated by Django 4.0.4 on 2022-05-28 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantapoma', '0011_athlete_born_player_score_alter_player_team_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='athlete',
            name='club',
            field=models.CharField(default='Società Canottieri Palermo', max_length=200),
        ),
    ]
