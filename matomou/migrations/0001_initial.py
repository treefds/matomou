# Generated by Django 5.1.1 on 2024-11-02 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VideoEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_title', models.CharField(max_length=250)),
                ('video_uploaded_at', models.DateTimeField(verbose_name='uploaded at')),
                ('video_uploader_name', models.CharField(max_length=250)),
                ('video_uploader_id', models.IntegerField()),
                ('main_url', models.CharField(max_length=250)),
                ('bilibili_id', models.CharField(max_length=40)),
                ('youtube_id', models.CharField(max_length=40)),
                ('niconico_id', models.CharField(max_length=40)),
                ('entry_created_at', models.DateTimeField(verbose_name='entry created at')),
                ('contributor_id', models.IntegerField()),
                ('video_description', models.CharField(max_length=10000)),
                ('video_credit', models.CharField(max_length=10000)),
            ],
        ),
    ]
