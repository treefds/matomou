from django.contrib import admin

# Register your models here.
from .models import VideoEntry, VideoList, VideoListEntry, Creator, Profile
admin.site.register(VideoEntry)
admin.site.register(VideoList)
admin.site.register(VideoListEntry)
admin.site.register(Creator)
admin.site.register(Profile)