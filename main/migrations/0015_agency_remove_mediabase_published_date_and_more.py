# Generated by Django 4.0.4 on 2022-05-20 07:11

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_mediabase_published_date_alter_video_genres'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='mediabase',
            name='published_date',
        ),
        migrations.RemoveField(
            model_name='mediabase',
            name='title',
        ),
        migrations.RemoveField(
            model_name='video',
            name='genres',
        ),
        migrations.AddField(
            model_name='mediabase',
            name='genres',
            field=models.ManyToManyField(related_name='media', to='main.genre', verbose_name='Genres'),
        ),
        migrations.AddField(
            model_name='mediabase',
            name='on_air_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Published Date'),
        ),
        migrations.AddField(
            model_name='mediabase',
            name='product_name',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Product Name'),
        ),
        migrations.AddField(
            model_name='mediabase',
            name='product_title',
            field=models.CharField(default='', max_length=256, verbose_name='Product Title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mediabase',
            name='production_company',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Production Company'),
        ),
        migrations.AlterField(
            model_name='mediabase',
            name='agency',
            field=models.CharField(default='', max_length=256, verbose_name='Agency'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mediabase',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='media', to='main.company', verbose_name='Company'),
        ),
        migrations.AlterField(
            model_name='mediabase',
            name='media_type',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, related_name='media', to='main.mediatype', verbose_name='Media Type'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mediabase',
            name='situations',
            field=models.ManyToManyField(related_name='media', to='main.situation', verbose_name='Situations'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_file',
            field=models.FileField(default='', upload_to='videos', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4', 'mov'])], verbose_name='Full Video'),
            preserve_default=False,
        ),
    ]