from .serializers import NoticeSerializer, BoardSerializer
from .models import Notice, Board
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.shortcuts import get_object_or_404


class NoticeList(ListAPIView):
    serializer_class = NoticeSerializer
    lookup_url_kwarg = "board_id"

    def get_queryset(self):
        board_id = self.kwargs.get(self.lookup_url_kwarg)
        notices = Notice.objects.filter(board_id=board_id).order_by('-num')
        return notices


class BoardUrl(RetrieveAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    lookup_field = 'board_id'

    def get_object(self):
        filter = {self.lookup_field: self.kwargs[self.lookup_field]}
        return get_object_or_404(self.queryset, **filter)
