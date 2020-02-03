from .serializers import NoticeSerializer
from .models import Notice
from rest_framework.generics import ListAPIView


class NoticeList(ListAPIView):
    serializer_class = NoticeSerializer
    lookup_url_kwarg = "board_id"

    def get_queryset(self):
        board_id = self.kwargs.get(self.lookup_url_kwarg)
        notices = Notice.objects.filter(board_id=board_id).order_by('-num')
        return notices
