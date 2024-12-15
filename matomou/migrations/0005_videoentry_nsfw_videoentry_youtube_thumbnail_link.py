# Generated by Django 5.1.1 on 2024-11-11 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matomou', '0004_videoentry_bilibili_thumbnail_link_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoentry',
            name='nsfw',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='videoentry',
            name='youtube_thumbnail_link',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]