from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view

from subtitles.models import Subtitle
from subtitles.serializers import SubtitleSerializer

# Create your views here.

@api_view(['GET', 'DELETE'])
def subtitles_list(request):
    # GET list of subtitles, POST a new subtitle, DELETE all subtitles

    if request.method == 'GET':
        subtitles = Subtitle.objects.all()

        subtitle_serializer = SubtitleSerializer(subtitles, many=True)
        return JsonResponse(subtitle_serializer.data, safe=False)
        
    elif request.method == 'DELETE':
        count = Subtitle.objects.all().delete()
        return JsonResponse({'message':'{} Subtitles were deleted sucessfully'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

# TODO: languages can be a query param here in form of an array. FIXME
@api_view(['GET', 'POST', 'DELETE'])
def subtitles_detail(request, video_id):
    # GET / POST / DELETE subtitle
    # indentify languages in the query param
    languages_str = request.GET.get('languages', None)
    if languages_str is not None:
        arr_languages = languages_str.replace(","," ").split()
        print(arr_languages)
    else:
        arr_languages = None
        print("No Language")
    
    if request.method == 'POST':
        # Get the subtitles for the video specified and the language specified in query params
        
        return JsonResponse({"message": "This is a test message. {}".format(arr_languages)})
      
    # find subtitles by video_id (and languages if provided)
    try: 
        subtitles = Subtitle.objects.filter(video_id=video_id)
        count = len(subtitles) 
    except Subtitle.DoesNotExist: 
        return JsonResponse({'message': 'The subtitles does not exist'}, status=status.HTTP_404_NOT_FOUND) 

    if request.method == 'GET':
        subtitles_serializer = SubtitleSerializer(subtitles)
        return JsonResponse(subtitles_serializer.data, many=True)
    
    
    
    elif request.method == 'DELETE':
        subtitles.delete()
        return JsonResponse({'message': ' {} Subtitles were deleted sucessfully'.format(count)}, status=status.HTTP_204_NO_CONTENT)

        