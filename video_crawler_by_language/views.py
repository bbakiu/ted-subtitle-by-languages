from django.shortcuts import render

from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
import coreapi
from bs4 import BeautifulSoup

# Create your views here.

@api_view(['GET'])
def videos_list(request, lang):
    base_url="https://www.ted.com"
    client = coreapi.Client()
    schema = client.get('https://www.ted.com/talks?sort=newest&language=sq')
    soup = BeautifulSoup(schema, "html.parser")
    nr_pages = soup.find_all("a", class_="pagination__item")[-1].get_text()
    all_video_links = []
    for i in range(int(nr_pages)):
        page_url = 'https://www.ted.com/talks?language=sq&page={}&sort=newest'.format(i+1)
        schema = client.get(page_url)
        soup = BeautifulSoup(schema, "html.parser")
        video_links = get_video_list(soup)
        all_video_links.extend(video_links)

    return JsonResponse({'message': 'There are {} pages of videos for the language {}. All video links: {}'.format(nr_pages, lang, all_video_links)}, status=status.HTTP_200_OK)

def get_video_list(page):
    base_url="https://www.ted.com"
    videosTagList = page.find_all("a", class_="ga-link", attrs={"data-ga-context" : "talks", "lang":True})
    video_links = []
    for videoTag in videosTagList:
        videoHref = videoTag.get("href")
        full_url = base_url + videoHref
        video_links.append(full_url)
    
    return video_links
    