from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view

from videos.models import Video
from videos.serializers import VideoSerializer
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