
from rest_framework import viewsets
from ..models import User,Quote
from ..serializers import UserSerializer,QuoteSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class UserViewSet (viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_backends = [
        DjangoFilterBackend,  # For exact matching filters
        filters.SearchFilter,  # For text search
        filters.OrderingFilter  # For sorting
    ]
    search_fields = ['username']
    ordering_fields = ['username', 'created_at']
    ordering = ['username']
    filterset_fields = ['username']

    @action(['get'],detail=True)
    def get_all_quotes(self,request,pk=None):
        try:
            user = self.get_object()
            quotes=Quote.objects.all()
            serializer = QuoteSerializer(quotes,many=true)
            return Response(serializer.data)

        except Exception as e:
              return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



