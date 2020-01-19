from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import NoticeView

notice = NoticeView.as_view({
    'get': 'list',
})

urlpatterns = format_suffix_patterns([
    path('<int:board_id>/', notice, name='notice'),
])
