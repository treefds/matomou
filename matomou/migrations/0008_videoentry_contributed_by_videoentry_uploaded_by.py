# Generated by Django 5.1.1 on 2024-11-11 18:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matomou', '0007_creator'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='videoentry',
            name='contributed_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contributed_entries', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='videoentry',
            name='uploaded_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uploaded_entries', to='matomou.creator'),
        ),
    ]