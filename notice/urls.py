from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import NoticeList, BoardUrl

urlpatterns = [
    path('notices/<int:board_id>/', NoticeList.as_view()),
    path('boards/<int:board_id>/', BoardUrl.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
