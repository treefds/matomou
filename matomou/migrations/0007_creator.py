# Generated by Django 5.1.1 on 2024-11-11 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matomou', '0006_videolist_videolistentry'),
    ]

    operations = [
        migrations.CreateModel(
            name='Creator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, max_length=20000)),
                ('bilibili_id', models.CharField(blank=True, max_length=100)),
                ('youtube_id', models.CharField(blank=True, max_length=100)),
                ('niconico_id', models.CharField(blank=True, max_length=100)),
                ('homepage_url', models.CharField(blank=True, max_length=250)),
                ('twitter_url', models.CharField(blank=True, max_length=250)),
                ('weibo_url', models.CharField(blank=True, max_length=250)),
                ('name_translations', models.TextField(blank=True, max_length=1000)),
                ('external_links', models.TextField(blank=True, max_length=1000)),
                ('avatar_url', models.CharField(blank=True, max_length=250)),
            ],
        ),
    ]
