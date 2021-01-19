from rest_framework import serializers
from subtitles.models import Subtitle

class SubtitleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subtitle
        fields = ('id',
                'videoId',
                'language',
                'contentJson',)