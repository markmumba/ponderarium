
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from django.urls import path, include
from ..views.quote import QuoteViewSet
from ..views.comment import CommentViewSet

router = DefaultRouter()
router.register(r'', QuoteViewSet,basename='quotes')

quote_router = NestedDefaultRouter(router, r'', lookup='quote')
quote_router.register(r'comments', CommentViewSet, basename="quote-comments")


urlpatterns = [
    path('', include(router.urls)),
    path('',include(quote_router.urls)),
]
