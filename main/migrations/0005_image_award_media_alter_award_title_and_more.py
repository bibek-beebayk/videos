# Generated by Django 4.0.4 on 2022-05-18 17:35

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_contributiontype_contributor_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('mediabase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.mediabase')),
                ('image_file', models.ImageField(upload_to='content/images/')),
            ],
            bases=('main.mediabase',),
        ),
        migrations.AddField(
            model_name='award',
            name='media',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Media', to='main.mediabase'),
        ),
        migrations.AlterField(
            model_name='award',
            name='title',
            field=models.CharField(max_length=256, verbose_name='Award Title'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_file_60',
            field=models.FileField(blank=True, null=True, upload_to='videos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4', 'mov'])], verbose_name='60 Seconds Preview'),
        ),
    ]
