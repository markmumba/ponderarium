
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from ..views.user import UserViewSet
from ..views.quote import QuoteViewSet

router = DefaultRouter()
router.register(r'',UserViewSet)

user_router = NestedDefaultRouter(router,r'',lookup='user');
user_router.register(r'quotes',QuoteViewSet,basename='user_quotes')

urlpatterns = [
    path('',include(router.urls)),
    path('',include(user_router.urls))
]
