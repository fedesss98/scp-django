# Generated by Django 4.1.2 on 2023-03-31 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.CharField(default='Lago Poma', max_length=80),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='url',
            field=models.CharField(default='https://canottaggioservice.canottaggio.net/menu_reg.php?reg=231301&&k1=R', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=80),
        ),
    ]