from django.shortcuts import render

from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
import coreapi
from bs4 import BeautifulSoup

import django_rq
from rq import Retry

from videos.tasks import save_video


# Create your views here.

@api_view(['GET'])
def ted_videos_list(request):
    origin_language = request.GET.get('origin_language', None)
    target_language = request.GET.get('target_language', None)
    client = coreapi.Client()
    schema = client.get('https://www.ted.com/talks?sort=newest&language={}'.format(origin_language))
    soup = BeautifulSoup(schema, "html.parser")
    nr_pages = soup.find_all("a", class_="pagination__item")[-1].get_text()
    all_video_details = []
    for i in range(int(nr_pages)):
        page_url = 'https://www.ted.com/talks?language=sq&page={}&sort=newest'.format(i + 1)
        schema = client.get(page_url)
        soup = BeautifulSoup(schema, "html.parser")
        video_details = get_video_list(soup, "{},{}".format(origin_language, target_language))
        all_video_details.extend(video_details)

    return JsonResponse(all_video_details, safe=False, status=status.HTTP_200_OK)

def get_video_list(page, languages):
    base_url="https://www.ted.com"
    videos_tag_list = page.find_all("a", class_="ga-link", attrs={"data-ga-context" : "talks", "lang":True})
    video_details = []
    for video_tag in videos_tag_list:
        videoHref = video_tag.get("href")
        full_url = base_url + videoHref
        normalized_url = query_string_remove(full_url)
        video_detail = {"url": normalized_url, "languages": languages}
        video_details.append(video_detail)
        job = django_rq.enqueue(func=save_video, args=[normalized_url, languages], retry=Retry(max=3, interval=[10, 30, 60]))

    return video_details

def query_string_remove(url):
    return  url[:url.find('?')] if url.find('?') > 0 else url

    