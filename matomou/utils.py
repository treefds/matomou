import requests, os, re

YOUTUBE_API_KEY = os.environ["YOUTUBE_API_KEY"] if "YOUTUBE_API_KEY" in os.environ else None

def get_video_site_and_id(url):
    if "youtube.com" in url:
        return ("youtube", get_youtube_video_id(url))
    elif "bilibili.com" in url:
        return ("bilibili", get_bilibili_video_id(url))
    return (None, None)



def get_youtube_video_details(video_id):
    if YOUTUBE_API_KEY == None:
        return None, None, None
    url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={YOUTUBE_API_KEY}'
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        data = response.json()
        if data['items']:
            video_title = data['items'][0]['snippet']['title']
            uploader_name = data['items'][0]['snippet']['channelTitle']
            published_at = data['items'][0]['snippet']['publishedAt']
            return video_title, uploader_name, published_at
    return None, None, None

def get_youtube_video_id(url):
    match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    return match.group(1) if match else None

def get_bilibili_video_id(url):
    match = re.search(r'\/(BV[0-9A-Za-z_-]{10}).*', url)
    return match.group(1) if match else None

def get_bilibili_video_details(video_id):
    url = 'https://api.bilibili.com/x/web-interface/view'
    print(video_id)
    if video_id[:2].lower() == "bv":
        params = { 'bvid': video_id }
    else:
        params = { 'aid': video_id }
    response = requests.get(url, headers={'User-Agent': 'matomou/v0.0.1', 'Accept': 'application/json'}, params=params, timeout=5)
    print(response)
    if response.status_code == 200:
        data = response.json()
        if data['data']:
            video_title = data['data']['title']
            uploader_name = data['data']['owner']['name']
            published_at = data['data']['pubdate']
            pic_url = data['data']['pic']
            return video_title, uploader_name, published_at, pic_url
    return None, None, None, None

def check_url_validity(url):
    url_regex = re.compile(
        r'^(https?://)?'                   # Optional http or https scheme
        r'(([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})' # Domain name (e.g., example.com)
        r'(:\d{1,5})?'                     # Optional port (e.g., :80)
        r'(/[^ ]*)?$'                      # Optional path (e.g., /path/to/page)
    )
    return bool(url_regex.match(url))