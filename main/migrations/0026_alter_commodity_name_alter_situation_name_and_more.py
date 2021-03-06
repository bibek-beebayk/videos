# Generated by Django 4.0.4 on 2022-05-25 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_alter_genre_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commodity',
            name='name',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='situation',
            name='name',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]
