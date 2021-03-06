# Generated by Django 4.0.4 on 2022-05-21 04:52

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fantapoma', '0005_race'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='time',
            field=models.DurationField(blank=True, default=datetime.timedelta(0), null=True),
        ),
        migrations.CreateModel(
            name='Special',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('special', models.TextField(blank=True, null=True)),
                ('points', models.IntegerField(default=0)),
                ('player', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
