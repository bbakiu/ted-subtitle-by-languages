from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view

from subtitles.models import Subtitle
from subtitles.serializers import SubtitleSerializer

import coreapi
import requests
import json


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


@api_view(['GET', 'POST', 'DELETE'])
def subtitles_detail(request, video_id):
    # GET / POST / DELETE subtitle
    # indentify languages in the query param
    languages_str = request.GET.get('languages', None)
    if languages_str is not None:
        languages_array = languages_str.replace(","," ").split()
    else:
        languages_array = None
    
    if request.method == 'POST':
        base_url = "http://www.ted.com/talks/subtitles/"
        # Get the subtitles for the video specified and the language specified in query params
        if languages_array is not None:
            for language in languages_array:
                try: 
                    existingSubtitle = Subtitle.objects.get(video_id=video_id, language=language)
                    id = existingSubtitle.pk
                except Subtitle.DoesNotExist:
                    id = None

                # print("Requests\n")
                full_url = base_url +  "id/{}/lang/{}".format(video_id, language)
                response_json = requests.get(full_url)
                # print(response_json.text)
                # print("====================\n")
                # print("Coreapi\n")
                # client = coreapi.Client()
                # schema = client.get(full_url)
                # print(schema)

                subtitles = json.loads(response_json.text)["captions"]
                save_subtitles = Subtitle(id=id, video_id=video_id, language=language, content_json=subtitles)
                save_subtitles.save()

            return JsonResponse({"message": "Subtitles for languages {} saved".format(languages_str)}, status=status.HTTP_200_OK)
        else :
            #throw error since language is required
            return JsonResponse({"message": "Languages are required. Please provide them as query param"}, status=status.HTTP_400_BAD_REQUEST)
        
    # find subtitles by video_id (and languages if provided) 
    subtitles = Subtitle.objects.filter(video_id=video_id)
    if languages_array is not None: 
        subtitles = Subtitle.objects.filter(video_id=video_id, language__in=languages_array)
    count = len(subtitles)

    if request.method == 'GET':
        
        subtitles_serializer = SubtitleSerializer(subtitles, many=True)
        return JsonResponse(subtitles_serializer.data, safe=False)
    
    elif request.method == 'DELETE':
        subtitles.delete()
        return JsonResponse({'message': ' {} Subtitles were deleted sucessfully'.format(count)}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def generate_files(request):
    if request.method == 'POST':
        assets_dir = "assets/"
        if assets_dir is None:
            raise ValueError("Assets directory does not exist")
        
        subtitles = Subtitle.objects.all()
        
        for subtitle in subtitles:
            filename = "{}VideoID-{}-{}.json".format(assets_dir, subtitle.video_id, subtitle.language)
            with open(filename, 'w') as file_object:
                file_object.write(json.dumps(subtitle.content_json))
                
        return JsonResponse({"message": "Files are written"}, status=status.HTTP_200_OK)      