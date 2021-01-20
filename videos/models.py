from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Video(models.Model):
    video_id = models.IntegerField(blank=False, default=0, primary_key = True)
    duration = models.CharField(max_length=70, blank=False, default='')
    speakers = ArrayField(models.CharField(max_length=200, blank=True),size=8)
    url = models.CharField(max_length=500, blank=False, default='')
    license_url = models.CharField(max_length=500, blank=False, default='')
    title = models.CharField(max_length=500, blank=False, default='')
    description = models.CharField(max_length=2500, blank=False, default='')
    viewed_count = models.IntegerField(blank=False, default=0)
    event = models.CharField(max_length=500, blank=False, default='')
    