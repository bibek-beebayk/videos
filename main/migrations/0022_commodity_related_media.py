# Generated by Django 4.0.4 on 2022-05-22 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_mediabase_created_at_mediabase_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='commodity',
            name='related_media',
            field=models.ManyToManyField(to='main.mediabase', verbose_name='Media'),
        ),
    ]