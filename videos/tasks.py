from django_rq import job
from videos.models import Video
from videos.serializers import VideoSerializer
import coreapi
from bs4 import BeautifulSoup
import json

import django_rq

from subtitles.tasks import save_subtitles

@job("default")
def save_video(url, languages) :
    client = coreapi.Client()
    normalized_url = query_string_remove(url)
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
    viewed_count = talk_meta["viewed_count"]
    event = talk_meta["event"]
    speakers = []
    for speaker in talk_meta["speakers"]:
        name = construct_name(speaker)
        speakers.append(name)
    
    video = Video(video_id=video_id, duration=duration, url=url, license_url=license_url, title=title, description=description, speakers=speakers, event=event, viewed_count=viewed_count)
    video.save()

    video_serializer = VideoSerializer(video)

    django_rq.enqueue(func=save_subtitles, args= [video_id, languages], result_ttl=5000)
    print(video_serializer.data)


def construct_name(speaker):
    return ' '.join(list(filter(None, [speaker["firstname"], speaker["middleinitial"], speaker["lastname"]])))


def query_string_remove(url):
    return  url[:url.find('?')] if url.find('?') > 0 else url