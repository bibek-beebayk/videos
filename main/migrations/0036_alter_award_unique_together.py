# Generated by Django 4.0.4 on 2022-05-26 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0035_alter_mediatype_name'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='award',
            unique_together=set(),
        ),
    ]