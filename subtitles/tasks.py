from subtitles.models import Subtitle
import requests
import json
from django_rq import job 

@job("default")
def save_subtitles(video_id, languages) :
    if languages is not None:
        languages_array = languages.replace(","," ").split()
    else:
        languages_array = None

    base_url = "http://www.ted.com/talks/subtitles/"
    # Get the subtitles for the video specified and the language specified in query params
    if languages_array is not None:
        for language in languages_array:
            try: 
                existingSubtitle = Subtitle.objects.get(video_id=video_id, language=language)
                id = existingSubtitle.pk
            except Subtitle.DoesNotExist:
                id = None

            full_url = base_url +  "id/{}/lang/{}".format(video_id, language)
            response_json = requests.get(full_url)

            subtitles =  json.loads(response_json.text)["captions"]
            save_subtitles = Subtitle(id=id, video_id=video_id, language=language, content_json=subtitles)
            save_subtitles.save()

        print("Subtitles for languages {} saved".format(languages))
    else :
        #throw error since language is required
        print("Languages are required. Please provide them as query param")