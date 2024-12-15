# Generated by Django 5.1.1 on 2024-11-02 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matomou', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoentry',
            name='video_title_translation',
            field=models.CharField(default='', max_length=20000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='videoentry',
            name='bilibili_id',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AlterField(
            model_name='videoentry',
            name='niconico_id',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AlterField(
            model_name='videoentry',
            name='video_credit',
            field=models.CharField(blank=True, max_length=20000),
        ),
        migrations.AlterField(
            model_name='videoentry',
            name='video_description',
            field=models.CharField(blank=True, max_length=20000),
        ),
        migrations.AlterField(
            model_name='videoentry',
            name='youtube_id',
            field=models.CharField(blank=True, max_length=40),
        ),
    ]