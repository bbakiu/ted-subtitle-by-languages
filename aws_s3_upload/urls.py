from django.conf.urls import url 
from aws_s3_upload import views

urlpatterns = [
    url(r'^api/assets/s3$', views.upload_file_to_s3),
]