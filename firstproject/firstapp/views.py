import requests
from isodate import parse_duration

from django.conf import settings
from django.shortcuts import render
# Create your views here.


def index(request):
    videos = []
    if request.method == 'POST':
        serach_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        serach_parmas = {
            'part': 'snippet',
            'q': request.POST['serach'],
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 9,
            'type': 'video',
        }

        video_ids = []
        r = requests.get(serach_url, params=serach_parmas)

        results = r.json()['items']

        for result in results:
            video_ids.append(result['id']['videoId'])

        video_parmas = {
            'key': settings.YOUTUBE_DATA_API_KEY,
            'part': 'snippet,contentDetails',
            'id': ','.join(video_ids),
            'maxResults': 9,
        }

        r = requests.get(video_url, params=video_parmas)

        results = r.json()['items']

        for result in results:
            video_data = {
                'title': result['snippet']['title'],
                'id': result['id'],
                'url': f'https://www.youtube.com/watch?v={result["id"]}',
                'duration': parse_duration(result['contentDetails']['duration']),
                'thumbnail': result['snippet']['thumbnails']['high']['url'],
            }

            videos.append(video_data)

    context = {
        'videos': videos
    }

    return render(request, 'firstapp/index.html', context=context)
