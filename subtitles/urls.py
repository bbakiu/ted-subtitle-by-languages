from django.conf.urls import url 
from subtitles import views

urlpatterns = [
    url(r'^api/subtitles$', views.subtitles_list),
    url(r'^api/subtitles/(?P<pk>[0-9]+)$', views.subtitles_detail),
]