from django.db import models
from django.db.models.constraints import UniqueConstraint

# Create your models here.

class Subtitle(models.Model):
    class Meta:
        constraints = [
            UniqueConstraint(fields=['video_id', 'language'], name="store_unique_video_lang_combination"),
        ]
    video_id = models.IntegerField(blank=False, default=0)
    language = models.CharField(max_length=70, blank=False, default='')
    content_json = models.JSONField(blank=True, default=dict)
   
