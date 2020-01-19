from rest_framework import serializers
from .models import Notice


class NoticeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notice
        fields = ['num', 'title', 'category', 'date', 'url']
