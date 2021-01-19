from django.conf.urls import url 
from subtitles import views

urlpatterns = [
    url(r'^api/subtitles$', views.subtitles_list),
    url(r'^api/subtitles/(?P<id>[0-9]+)$', views.subtitles_detail),
]