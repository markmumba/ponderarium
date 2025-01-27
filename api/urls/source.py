from django.urls import path
from ..views.source import source_detail

urlpatterns = [
    path('<uuid:pk>/',source_detail,name='source-detail')
]