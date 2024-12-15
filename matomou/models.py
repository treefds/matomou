from django.db import models
from django.contrib.auth.models import User

from .utils import get_video_site_and_id

class VideoList(models.Model):
    # A collection of videos, each entry containing:
    #  - A video ID;
    #  - A display coordinate (x, y, z); only x is actually used. 
    #  - A write-up. Markdown Supported?
    # And Metadata for the list itself:
    #  - owner_id: who owns this repo. 
    #  - public_level: The larger the number, the less people can view it;
    #    - 0: public
    #    - 1: login
    #    - 2: follower
    #    - 3: friends
    #    - 4: private
    #  - List name
    #  - List Description
    #  - List Thumbnail? Maybe not
    #  - List created_at
    #  - List updated_at

    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, max_length=20000)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="video_lists")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    public_level = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Creator(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=20000, blank=True)
    
    bilibili_id = models.CharField(max_length=100, blank=True)
    youtube_id = models.CharField(max_length=100, blank=True)
    niconico_id = models.CharField(max_length=100, blank=True)

    homepage_url = models.URLField(max_length=250, blank=True)
    twitter_url = models.URLField(max_length=250, blank=True)
    weibo_url = models.URLField(max_length=250, blank=True)

    name_translations = models.TextField(max_length=1000, blank=True)
    external_links = models.TextField(max_length=1000, blank=True)

    avatar_url = models.URLField(max_length=250, blank=True)


class VideoEntry(models.Model):
    # Video Info
    video_title = models.CharField(max_length=250)
    video_title_translation = models.CharField(max_length=20000, blank=True)
    video_uploaded_at = models.DateTimeField("uploaded at")
    video_uploader_name = models.CharField(max_length=250)
    video_uploader_id = models.IntegerField()

    # Link to video
    main_url = models.URLField(max_length=250)
    bilibili_id = models.CharField(max_length=40, blank=True)
    youtube_id = models.CharField(max_length=40, blank=True)
    niconico_id = models.CharField(max_length=40, blank=True)

    # Details about the entry
    entry_created_at = models.DateTimeField("entry created at")
    contributor_id = models.IntegerField()

    # Extra information, user-transcribed
    video_description = models.CharField(max_length=20000, blank=True)
    video_credit = models.CharField(max_length=20000, blank=True)

    # Assistive Links - Thumbnail URL
    bilibili_thumbnail_link = models.URLField(max_length=250, blank=True)
    niconico_thumbnail_link = models.URLField(max_length=250, blank=True)
    youtube_thumbnail_link  = models.URLField(max_length=250, blank=True)

    # Tag
    nsfw = models.BooleanField(default=False)

    # Contributor and Uploader ForeignKey
    contributed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contributed_entries", null=True)
    uploaded_by = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name="uploaded_entries", null=True)

    def __str__(self):
        return self.video_title
    
    @classmethod
    def find_video(cls, url):
        site, video_id = get_video_site_and_id(url)
        if not site or not video_id:
            return None
        if site == "youtube":
            return cls.objects.get(youtube_id=video_id)
        elif site == "bilibili":
            return cls.objects.get(bilibili_id=video_id)
        return None

class VideoListEntry(models.Model):
    video_list = models.ForeignKey(VideoList, on_delete=models.CASCADE, related_name="entries")
    
    video = models.ForeignKey(VideoEntry, on_delete=models.CASCADE, related_name="related_list_entries")
    order_x = models.IntegerField(default=0)
    order_y = models.IntegerField(default=0)
    order_z = models.IntegerField(default=0)
    writeup = models.TextField(blank=True, max_length=10000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.video_list}({self.video})"



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_url = models.URLField(blank=True)

    def __str__(self):
        return self.user.username