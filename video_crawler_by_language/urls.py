from django.conf.urls import url
from video_crawler_by_language import views

urlpatterns = [
    url(r'^api/ted/videos$', views.ted_videos_list),
]