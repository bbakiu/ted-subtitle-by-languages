from django.conf.urls import url
from video_crawler_by_language import views

urlpatterns = [
    url(r'^api/languages/(?P<lang>[a-z]+)$', views.videos_list),
]