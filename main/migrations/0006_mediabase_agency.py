# Generated by Django 4.0.4 on 2022-05-19 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_image_award_media_alter_award_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediabase',
            name='agency',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
