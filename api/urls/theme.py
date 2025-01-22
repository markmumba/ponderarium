from rest_framework.routers import DefaultRouter
from django.urls import path, include
from ..views.theme import ThemeViewSet

# Create a router and register our viewset
router = DefaultRouter()
router.register(r'', ThemeViewSet)

# The router will generate URLs for us
urlpatterns = [
    path('', include(router.urls)),
]