# Generated by Django 4.0.4 on 2022-05-20 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_alter_award_media_alter_mediabase_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='vtt_url',
        ),
    ]