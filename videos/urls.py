from django.conf.urls import url
from videos import views

urlpatterns = [
    url(r'^api/videos$', views.videos_list),
    url(r'^api/videos/(?P<video_id>[0-9]+)$', views.videos_detail),
    url(r'^api/videos/url$', views.video_detail_by_url),

]