
from ..models import Quote
from ..serializers import QuoteSerializer, CommentSerializer,QuoteListSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class QuoteViewSet(viewsets.ModelViewSet):

    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer

    filter_backends = [
        DjangoFilterBackend,  
        filters.SearchFilter,  
        filters.OrderingFilter  
    ]
    search_fields = ['content']  
    ordering_fields = ['content', 'created_at']  
    ordering = ['content']  
    filterset_fields = ['content']

    def get_serializer_class(self):
        if self.action == "list":
            return QuoteListSerializer
        return QuoteSerializer

    
    @action(detail=True, methods=['get', 'post'])
    def comments(self, request, pk=None):

        quote = self.get_object()

        if request.method == 'GET':
            comments = quote.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(quote=quote)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    



