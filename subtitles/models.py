from django.db import models

# Create your models here.

class Subtitle(models.Model):
    videoId = models.IntegerField(blank=False, default=0)
    language = models.CharField(max_length=70, blank=False, default='')
    contentJson= models.JSONField(blank=True, default=dict)
