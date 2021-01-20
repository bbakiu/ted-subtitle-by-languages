from rest_framework import serializers
from videos.models import Video

class VideoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Video
        fields = ('id',
                'video_id',
                'duration',
                'speakers',
                'url',
                'license_url',
                'title',
                'description',
                'event',
                'viewed_count',)