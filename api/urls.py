from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter


from .views import ThemeViewSet, QuoteViewSet, UserViewSet, CommentViewSet,UpvoteViewSet, source_detail

router = DefaultRouter()
router.register(r'themes', ThemeViewSet, basename='themes')
router.register(r'users', UserViewSet, basename='users')
router.register(r'quotes', QuoteViewSet, basename='quotes')
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'upvotes',UpvoteViewSet,basename='upvotes')

user_quotes_router = NestedDefaultRouter(router, r'users', lookup='user')
user_quotes_router.register(r'quotes', QuoteViewSet, basename='user-quotes')

quote_comments_router = NestedDefaultRouter(router, r'quotes', lookup='quote')
quote_comments_router.register(
    r'comments', CommentViewSet, basename='quote-comments')

comment_upvote_router = NestedDefaultRouter(router,r'comments',lookup='comment')
comment_upvote_router.register(r'upvotes',UpvoteViewSet,basename='quote-upvotes')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(user_quotes_router.urls)),
    path('', include(quote_comments_router.urls)),
    path('',include(comment_upvote_router.urls)),
    path('<uuid:pk>/', source_detail, name='source-detail')
]
