# Generated by Django 4.0.4 on 2022-05-21 04:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fantapoma', '0004_remove_athlete_player_athlete_player'),
    ]

    operations = [
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('location', models.CharField(max_length=200)),
                ('event', models.CharField(max_length=200)),
                ('result', models.CharField(max_length=20)),
                ('time', models.DurationField()),
                ('boat', models.CharField(max_length=100)),
                ('cat', models.CharField(max_length=50)),
                ('soc', models.CharField(max_length=100)),
                ('athlete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fantapoma.athlete')),
            ],
        ),
    ]
