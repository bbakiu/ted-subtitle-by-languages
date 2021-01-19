from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from subtitles.models import Subtitle
from subtitles.serializers import SubtitleSerializer
from rest_framework.decorators import api_view

# Create your views here.

@api_view(['GET','POST', 'DELETE'])
def subtitles_list(request):
    # GET list of subtitles, POST a new subtitle, DELETE a subtitle

    if request.method == 'GET':
        subtitles = Subtitle.objects.all()

        subtitle_serializer = SubtitleSerializer(subtitles, many=True)
        return JsonResponse(subtitle_serializer.data, safe=False)
    
    elif request.method == 'POST':
        subtitle_data = JSONParser().parse(request)
        subtitle_serializer = SubtitleSerializer(data=subtitle_data)
        if subtitle_serializer.is_valid():
            subtitle_serializer.save()
            print(subtitle_serializer.data)
            return JsonResponse(subtitle_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(subtitle_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = Subtitle.objects.all().delete()
        return JsonResponse({'message':'{} Subtitles were deleted sucessfully'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def subtitles_detail(request, pk):
    # find subtitle by pk (id)
    try: 
        subtitle = Subtitle.objects.get(pk=pk) 
    except Subtitle.DoesNotExist: 
        return JsonResponse({'message': 'The subtitle does not exist'}, status=status.HTTP_404_NOT_FOUND) 
        
    # GET / PUT / DELETE subtitle
    if request.method == 'GET':
        subtitle_serializer = SubtitleSerializer(subtitle)
        return JsonResponse(subtitle_serializer.data)
    
    elif request.method == 'PUT':
        subtitle_data = JSONParser().parse(request)
        subtitle_serializer = SubtitleSerializer(subtitle, data=subtitle_data)
        if subtitle_serializer.is_valid():
            subtitle_serializer.save()
            return JsonResponse(subtitle_serializer.data)
        return JsonResponse(subtitle_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        subtitle.delete()
        return JsonResponse({'message': 'Subtitle was deleted sucessfully'}, status=status.HTTP_204_NO_CONTENT)

        