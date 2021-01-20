from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view

from videos.models import Video
from videos.serializers import VideoSerializer
import coreapi
from bs4 import BeautifulSoup
import json
# Create your views here.


@api_view(['GET','POST', 'DELETE'])
def videos_list(request):
    # GET list of videos, DELETE all videos, POST all video

    if request.method == 'GET':
        videos = Video.objects.all()

        videos_serializer = VideoSerializer(videos, many=True)
        return JsonResponse(videos_serializer.data, safe=False)

    elif request.method == 'POST':
        video_data = JSONParser().parse(request)
        video_serializer = VideoSerializer(data=video_data)

        if video_serializer.is_valid():
            video_serializer.save()
            return JsonResponse(video_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(video_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Video.objects.all().delete()
        return JsonResponse({'message': '{} Videos were deleted successfully'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
def videos_detail(request, id):
    #find a video by id
    try:
        video = Video.objects.get(pk=id)
    except Video.DoesNotExist:
        return JsonResponse({'message': 'The video does not exist'}, status=status.HTTP_404_NOT_FOUND)
    # GET a videos, DELETE a videos, PUT a video
    if request.method == 'GET':
        video_serializer = VideoSerializer(video)
        return JsonResponse(video_serializer.data)
    
    elif request.method == 'PUT':
        video_data = JSONParser().parse(request)
        video_serializer = VideoSerializer(video, data=video_data)
        if video_serializer.is_valid():
            video_serializer.save()
            return JsonResponse(video_serializer.data)
        return JsonResponse(video_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        video.delete()
        return JsonResponse({'message': 'Video was deleted sucessfully'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def video_detail_by_url(request):
    video_link =  JSONParser().parse(request)
    client = coreapi.Client()
    normalized_url = query_string_remove(video_link["url"])
    print(video_link["url"])
    print (normalized_url)
    schema = client.get(normalized_url)

    soup = BeautifulSoup(schema, "html.parser")
    video_meta_unprocessed = soup.find("div", attrs={"itemscope":True, "itemtype":"https://schema.org/VideoObject"})
    video_meta = BeautifulSoup(str(video_meta_unprocessed), "html.parser")

    duration = video_meta.find("meta", attrs={"itemprop":"duration"})["content"]
    license_url = video_meta.find("link", attrs={"itemprop":"license"})["href"]
    title = video_meta.find("meta", attrs={"itemprop":"name"})["content"]
    description = video_meta.find("meta", attrs={"itemprop":"description"})["content"]

    script_unprocessed = str(soup.find("script", attrs={"data-spec":"q"}))
    openIndex = script_unprocessed.index('{')
    closeIndex=script_unprocessed.rindex('}')

    jsonSubstring = script_unprocessed[openIndex:closeIndex + 1]
    talk_meta = json.loads(jsonSubstring)["__INITIAL_DATA__"]

    video_id = talk_meta["current_talk"]
    url = talk_meta["url"]
    speakers = []
    for speaker in talk_meta["speakers"]:
        name = construct_name(speaker)
        speakers.append(name)
    
    video = Video(video_id=video_id, duration=duration, url=url, license_url=license_url, title=title, description=description, speakers=speakers)
    video.save()
    print(video)
    video_serializer = VideoSerializer(video)
    return JsonResponse(video_serializer.data, status=status.HTTP_200_OK)

def query_string_remove(url):
    return  url[:url.find('?')] if url.find('?') > 0 else url

def construct_name(speaker):
    return ' '.join(list(filter(None, [speaker["firstname"], speaker["middleinitial"], speaker["lastname"]])))

