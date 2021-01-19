from django.conf.urls import url
from videos import views

urlpatterns = [
    url(r'^api/videos$', views.videos_list),
    url(r'^api/videos/(?P<id>[0-9]+)$', views.videos_detail),
]