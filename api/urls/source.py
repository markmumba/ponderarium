from django.urls import path
from ..views.source import source_list,source_detail

urlpatterns = [
    path('',source_list),
    path('<uuid:pk>/',source_detail)
]