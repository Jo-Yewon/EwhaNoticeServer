from rest_framework import serializers
from .models import Notice, Board


class NoticeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notice
        fields = ['num', 'title', 'category', 'date', 'url']


class BoardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Board
        fields = ['base_url', 'next_url']
