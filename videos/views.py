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
    schema = client.get(video_link["url"])
    soup = BeautifulSoup(schema, "html.parser")
    video_meta = soup.find("div", attrs={"itemscope":True, "itemtype":"https://schema.org/VideoObject"})
    # print("\n=======\n")
    # print(video_meta)
    # print("\n=======\n")
    script = str(soup.find("script", attrs={"data-spec":"q"}))
    # print("\n=======\n")
    # print(script)
    # print("\n=======\n")
    soup2 = BeautifulSoup(str(video_meta), "html.parser")
    # print(soup2)
   
    duration = soup2.find("meta", attrs={"itemprop":"duration"})["content"]
    
    url = video_link["url"]
    licenseUrl = soup2.find("link", attrs={"itemprop":"license"})["href"]
    title = soup2.find("meta", attrs={"itemprop":"name"})["content"]
    description = soup2.find("meta", attrs={"itemprop":"description"})["content"]
    print(duration, url, licenseUrl, title, description)
    openIndex = script.index('{')
    closeIndex=script.rindex('}')
    print('Found open index {} and close index {}'.format(openIndex, closeIndex))
    substring = script[openIndex:closeIndex+1]
    talk_meta = json.loads(substring)["__INITIAL_DATA__"]
    print('Json content is {} '.format(talk_meta))
    # videoId=talk_meta["current_talk"]
    # author=talk_meta.speakers[0]["firstname"]
    # author = soup2.find("span", attrs={"itemprop":"author"}).children
    # print(videoId,"\n", author)
    


    return JsonResponse(talk_meta, status=status.HTTP_200_OK)
