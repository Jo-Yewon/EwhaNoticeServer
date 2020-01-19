from rest_framework import serializers
from .models import Notice


class NoticeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notice
        fields = ['board_id', 'num', 'title', 'category', 'date', 'url']
