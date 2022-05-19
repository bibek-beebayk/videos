# Generated by Django 4.0.4 on 2022-05-19 08:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_remove_mediabase_genre_video_genre_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='vtt_url',
            field=models.URLField(blank=True, max_length=1024, null=True, verbose_name='VTT URL'),
        ),
        migrations.AlterField(
            model_name='mediabase',
            name='published_date',
            field=models.DateField(default=datetime.datetime(2021, 5, 19, 8, 32, 37, 854235, tzinfo=utc), verbose_name='Published Date'),
        ),
    ]