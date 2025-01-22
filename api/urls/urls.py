
from django.urls import path, include


urlpatterns = [
    path('themes/', include('api.urls.theme')),
    path('source/', include('api.urls.source'))
]
