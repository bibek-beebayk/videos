# Generated by Django 4.0.4 on 2022-05-20 05:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_mediabase_published_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediabase',
            name='published_date',
            field=models.DateField(default=datetime.datetime(2021, 5, 20, 5, 19, 4, 884195, tzinfo=utc), verbose_name='Published Date'),
        ),
    ]
