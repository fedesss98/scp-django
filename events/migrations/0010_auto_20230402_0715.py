# Generated by Django 4.1.2 on 2023-04-02 05:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20230402_0715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='url',
            field=models.CharField(default=uuid.uuid4, max_length=200, unique=True),
        )
    ]
