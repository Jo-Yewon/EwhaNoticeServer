from rest_framework import viewsets
from .serializers import NoticeSerializer
from .models import Notice


class NoticeView(viewsets.ModelViewSet):
    lookup_field = 'board_id'
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

