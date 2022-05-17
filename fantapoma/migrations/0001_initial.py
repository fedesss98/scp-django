# Generated by Django 3.2.5 on 2022-05-02 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Athlete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('total', models.IntegerField(default=0, verbose_name='Total Races')),
                ('first', models.IntegerField(default=0)),
                ('second', models.IntegerField(default=0)),
                ('third', models.IntegerField(default=0)),
                ('first_time', models.DateTimeField(verbose_name='First Race Date')),
                ('last_time', models.DateTimeField(verbose_name='Last Race Date')),
                ('points', models.IntegerField(default=0)),
            ],
        ),
    ]
