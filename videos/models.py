from django.db import models

# Create your models here.
class Video(models.Model):
    videoId = models.IntegerField(blank=False, default=0)
    duration = models.CharField(max_length=70, blank=False, default=''),
    author= models.CharField(max_length=250, blank=False, default=''),
    url = models.CharField(max_length=500, blank=False, default=''),
    licenseUrl = models.CharField(max_length=500, blank=False, default=''),
    title = models.CharField(max_length=500, blank=False, default=''),
    description = models.CharField(max_length=2500, blank=False, default=''),
    