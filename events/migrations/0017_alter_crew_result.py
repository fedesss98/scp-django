# Generated by Django 4.1.2 on 2024-02-03 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_crew_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crew',
            name='result',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]