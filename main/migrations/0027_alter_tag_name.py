# Generated by Django 4.0.4 on 2022-05-25 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_alter_commodity_name_alter_situation_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=256),
        ),
    ]
