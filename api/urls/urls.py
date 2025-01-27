
from django.urls import path, include


urlpatterns = [
    path('themes/', include('api.urls.theme')),
    path('sources/', include('api.urls.source')),
    path('quotes/', include('api.urls.quote')),
    path('comments/', include('api.urls.comment'))

]
