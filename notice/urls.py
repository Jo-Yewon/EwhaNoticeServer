from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import NoticeList

urlpatterns = [
    path('notices/<int:board_id>/', NoticeList.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
