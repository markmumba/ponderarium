
from rest_framework.routers import DefaultRouter
from django.urls import path,include 
from ..views.comment import CommentViewSet


router= DefaultRouter()

router.register(r'',CommentViewSet,basename='comment')

urlpatterns = [
    path('',include(router.urls)),
]
