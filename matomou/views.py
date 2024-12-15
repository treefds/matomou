from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.contrib.auth.decorators import login_required

from datetime import datetime

from .models import VideoEntry, VideoList, VideoListEntry
from .utils import get_youtube_video_details, get_youtube_video_id, get_bilibili_video_id, get_bilibili_video_details

from enum import Enum


class CreateEntryCode(Enum):
    SUCCESS = 0
    BAD_URL = 1
    DUPLICATE_UPLOAD = 2
    REMOTE_FAILED = 3
    UNSUPPORTED_URL = 4

def index(request):

    listed_video_entries = VideoEntry.objects.all().order_by('-id')[:10]   # TODO: is this the most efficient SQL query?

    # Clean up data before sent as context to render template.
    cleaned_video_entries = []
    for entry in listed_video_entries:
        cleaned_video_entries.append(
            {
                "id": entry.id, 
                "video_title": entry.video_title, 
                "video_uploader_name": entry.video_uploader_name, 
                "youtube_id": entry.youtube_id,
                "bilibili_id": entry.bilibili_id,
                "main_url": entry.main_url, 
                "thumbnail_url": f"https://i.ytimg.com/vi/{entry.youtube_id}/hqdefault.jpg" if "youtube" in entry.main_url else entry.bilibili_thumbnail_link,
                "url_site": "youtube" if "youtube" in entry.main_url else "bilibili" if "bilibili" in entry.main_url else "niconico"
            }
        )
    
    # Create Video lists
    listed_video_lists = VideoList.objects.all().order_by('-id')[:10]  # TODO: is this the most efficient SQL query?

    # Clean Up
    cleaned_video_lists = []
    for vlist in listed_video_lists:
        list_entries = vlist.entries.all()    # TODO: This may cost some time!
        if not list_entries:
            continue
        lentry = list_entries[0]
        cleaned_video_lists.append(
            {
                "id": vlist.id, 
                "list_name": vlist.name, 
                "thumbnail_url": f"https://i.ytimg.com/vi/{lentry.video.youtube_id}/hqdefault.jpg" if "youtube" in lentry.video.main_url else lentry.video.bilibili_thumbnail_link
            }
        )

    context = {"video_entries": cleaned_video_entries, "video_lists": cleaned_video_lists}
    return render(request, "matomou/index.html", context)


def video_detail(request, vdid : int):
    try:
        entry = VideoEntry.objects.get(id=vdid)
    except Exception as e:
        return HttpResponse("Bad Request", status_code=400)
    if not entry:
        return HttpResponse("Bad Request", status_code=400)
    video = {
        "thumbnail_url": f"https://i.ytimg.com/vi/{entry.youtube_id}/hqdefault.jpg" if "youtube" in entry.main_url else entry.bilibili_thumbnail_link, 
        "video_title": entry.video_title, 
        "video_uploader_name": entry.video_uploader_name, 
        "main_url": entry.main_url, 
        "youtube_id": entry.youtube_id, 
        "bilibili_id": entry.bilibili_id
    }

    return render(request, "matomou/video_detail.html", {"video_entry": video})


def create_video_list(request):
    return render(request, "matomou/create_video_list.html")


def call_create_video_list(request):
    if request.method != "POST":
        return HttpResponse("Bad Request", status=400)
    
    list_name = request.POST.get("list_name")
    list_description = request.POST.get("list_description")
    public_level = request.POST.get("public_level")

    if not list_name or not list_description:
        return HttpResponse("No Input, bad request", status=400)
    

    vlist = VideoList.objects.create(
        name=list_name, 
        description=list_description, 
        owner=request.user, 
        public_level=public_level
    )

    return redirect("matomou:video_list", listid=vlist.id)

@login_required
def edit_video_list(request, listid : int):
    vlist = VideoList.objects.get(id=listid)
    if not vlist:
        return Http404()
    context = {
        "list_id": listid, 
        "list_description": vlist.description, 
        "list_name": vlist.name, 
        "public_level": vlist.public_level
    }
    return render(request, "matomou/edit_video_list.html", context=context)

@login_required
def call_edit_video_list(request, listid : int):
    if request.method != "POST":
        return HttpResponse("Bad Request", status=400)
    
    list_name = request.POST.get("list_name")
    list_description = request.POST.get("list_description")
    public_level = request.POST.get("public_level")

    if not list_name or not list_description:
        return HttpResponse("No Input, bad request", status=400)
    
    vlist = VideoList.objects.get(id=listid)
    if not vlist:
        return Http404()
    
    if vlist.owner != request.user:
        return HttpResponse("Access denied! User not owner of the List", status=403)

    vlist.name = list_name
    vlist.description = list_description
    vlist.public_level = public_level
    vlist.save()

    return redirect("matomou:video_list", listid=vlist.id)






def video_list(request, listid: int):
    thelist = VideoList.objects.get(id=listid)
    if not thelist:
        return HttpResponse("Bad Request", status=400)
    listed_video_list_entries = thelist.entries.all().order_by('order_x')

    # Clean up data before sent as context to render template.
    cleaned_video_entries = []
    for list_entry in listed_video_list_entries:
        entry = list_entry.video
        cleaned_video_entries.append(
            {
                "id": entry.id, 
                "video_title": entry.video_title, 
                "video_uploader_name": entry.video_uploader_name, 
                "writeup": list_entry.writeup, 
                "order": list_entry.order_x, 
                "youtube_id": entry.youtube_id,
                "bilibili_id": entry.bilibili_id,
                "main_url": entry.main_url, 
                "thumbnail_url": f"https://i.ytimg.com/vi/{entry.youtube_id}/hqdefault.jpg" if "youtube" in entry.main_url else entry.bilibili_thumbnail_link,
                "url_site": "youtube" if "youtube" in entry.main_url else "bilibili" if "bilibili" in entry.main_url else "niconico"
            }
        )

    context = {
        "video_entries": cleaned_video_entries, 
        "list_id": thelist.id,
        "list_name": thelist.name, 
        "list_description": thelist.description
    }

    return render(request, "matomou/video_list.html", context)
    

@login_required
def create_entry(request):
    return render(request, "matomou/create_entry.html")

@login_required
def call_create_entry(request):
    # Expected Response:
    # <QueryDict: {'csrfmiddlewaretoken': ['<--token-->'], 'video_url': ['https://www.youtube.com/watch?v=ABCDEFGHIJK']}>
    video_url = request.POST.get("video_url")
    if not video_url:
        return HttpResponse("Parsing Error: Received URL is empty.", status=400)
    video_url : str = video_url.strip()
    video_url = video_url.replace("http://", "")
    video_url = video_url.replace("https://", "")

    if "youtube.com/" in video_url:
        code = _create_youtube_entry(video_url)
    elif "bilibili.com/" in video_url:
        code = _create_bilibili_entry(video_url)
    else:
        code = CreateEntryCode.UNSUPPORTED_URL
    
    match code:
        case CreateEntryCode.SUCCESS:
            return HttpResponse("Success!")
        case CreateEntryCode.UNSUPPORTED_URL:
            return HttpResponse("Site is not supported yet!", status=400)
        case CreateEntryCode.BAD_URL:
            return HttpResponse("URL cannot be parsed!", status=400)
        case CreateEntryCode.REMOTE_FAILED:
            return HttpResponse("Failed to retrieve video data from remote site!", status=400)
        case CreateEntryCode.DUPLICATE_UPLOAD:
            return HttpResponse("The video has been uploaded!")

@login_required
def add_to_list(request, vlist_id : int):
    context = {"video_list_id": vlist_id}
    return render(request, "matomou/create_entry.html")

@login_required
def call_add_to_list(request, listid : int):
    video_url = request.POST.get("video_url")
    # --- vlist_id = request.POST.get("video_list_id")
    if not video_url or not listid:
        return HttpResponse("Parsing Error: Received URL is empty.", status=400)
    
    video_url : str = video_url.strip()
    video_url = video_url.replace("http://", "")
    video_url = video_url.replace("https://", "")

    if "youtube.com/" in video_url:
        code = _create_youtube_entry(video_url)
    elif "bilibili.com/" in video_url:
        code = _create_bilibili_entry(video_url)
    else:
        code = CreateEntryCode.UNSUPPORTED_URL
    
    if code not in (CreateEntryCode.DUPLICATE_UPLOAD, CreateEntryCode.SUCCESS):
        return HttpResponse("Creation Failed!!")
    
    try:
        video = VideoEntry.find_video(video_url)
        vlist = VideoList.objects.get(id=listid)
    except Exception as e:
        print(e)
        return HttpResponse("Unknown video / video list!", status=400)
    
    VideoListEntry.objects.create(
        video=video, 
        video_list=vlist
    )
    return redirect("matomou:video_list", listid=listid)

@login_required
def call_remove_from_list(request, listid : int, vdid : int):
    if request.method != "POST":
        return HttpResponse("Invalid request method: POST required", status=400)
    
    query = VideoListEntry.objects.filter(video_list_id=listid, video_id=vdid)
    if not query:
        return HttpResponse("No entry matches conditions.")
    list_entry = query.first()
    list_entry.delete()

    return HttpResponse("Success!")

@login_required
def edit_list_entry(request, listid : int, vdid : int):
    vlentry = VideoListEntry.objects.filter(video_id=vdid, video_list_id=listid).first()
    if not vlentry:
        return HttpResponse("Video List Entry deos not exist", status=400)
    
    writeup = vlentry.writeup
    context = {
        "list_id": listid, 
        "video_id": vdid, 
        "writeup": writeup
    }
    return render(request, "matomou/edit_list_entry.html", context=context)


@login_required
def call_edit_list_entry(request, listid : int, vdid : int):
    if request.method != "POST":
        return HttpResponse("Invalid request method: POST required", status=400)
    
    vlentry = VideoListEntry.objects.filter(video_id=vdid, video_list_id=listid).first()
    if not vlentry:
        return HttpResponse("Video List Entry deos not exist", status=400)
    
    writeup = request.POST.get("writeup")
    if not writeup:
        return HttpResponse("Bad Request", status=400)

    vlentry.writeup = writeup
    vlentry.save()
    
    return redirect("matomou:video_list", listid=listid)


def _create_youtube_entry(video_url):
    # TODO: URL Sanity Check
    _components = video_url.split("youtube.com/watch?v=")
    # First round Check
    if len(_components) != 2 or len(_components[-1]) != 11:
        return CreateEntryCode.BAD_URL
    # Second Round Check
    video_id = get_youtube_video_id(video_url)
    if not video_id:
        return CreateEntryCode.BAD_URL
    # Check if this has been uploaded
    if VideoEntry.objects.filter(youtube_id=video_id):
        return CreateEntryCode.DUPLICATE_UPLOAD

    # Check Success. Get Data from YouTube API
    video_title, uploader_name, uploaded_at = get_youtube_video_details(video_id)
    if not (video_title and uploader_name):
        return CreateEntryCode.REMOTE_FAILED

    VideoEntry.objects.create(
        video_title=video_title, 
        video_uploaded_at=uploaded_at, 
        video_uploader_name=uploader_name, 
        video_uploader_id=-1, 
        main_url=video_url, 
        youtube_id=video_id, 
        entry_created_at=datetime.now(), 
        contributor_id=1
    )
    return CreateEntryCode.SUCCESS

def _create_bilibili_entry(video_url):
    # TODO: URL Sanity Check
    video_id = get_bilibili_video_id(video_url)
    if not video_id:
        return CreateEntryCode.BAD_URL
    # Check if this has been uploaded
    if VideoEntry.objects.filter(bilibili_id=video_id):
        return CreateEntryCode.DUPLICATE_UPLOAD
    # Check succeed, get data
    video_title, uploader_name, uploaded_at, thumbnail_url = get_bilibili_video_details(video_id)
    if not video_title:
        return CreateEntryCode.REMOTE_FAILED
    uploaded_at = datetime.fromtimestamp(uploaded_at)
    VideoEntry.objects.create(
        video_title=video_title, 
        video_uploaded_at=uploaded_at, 
        video_uploader_name=uploader_name, 
        video_uploader_id=-1, 
        main_url=video_url, 
        bilibili_id=video_id, 
        entry_created_at=datetime.now(), 
        contributor_id=1, 
        bilibili_thumbnail_link=thumbnail_url
    )
    return CreateEntryCode.SUCCESS

def _route_youtube_thumbnail_url(video_id):
    return f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"





# ----------------

def about_me(request):
    return render(request, "matomou/about.html")

@login_required
def api_bvid_proxy(request):
    if not request.method == "GET":
        return JsonResponse({"error": "Not a GET request!"}, status=400)
    bvid = request.GET.get("bvid")
    if not bvid:
        return JsonResponse({"error": "BVID not available"}, status=400)
    video_title, uploader_name, published_at, pic_url = get_bilibili_video_details(bvid)

    response_data = {
        "bvid": bvid, 
        "video_title": video_title, 
        "uploader_name": uploader_name,
        "published_at": published_at, 
        "pic_url": pic_url
    }
    return JsonResponse(response_data)