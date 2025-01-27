
from ..models import Quote
from ..serializers import QuoteSerializer, CommentSerializer, SourceSerializer

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
    search_fields = ['name']  
    ordering_fields = ['name', 'created_at']  
    ordering = ['name']  
    filterset_fields = ['name']

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

    

    @action(detail=True, methods=['post'])
    def source(self, request, pk=None):
    
        quote = self.get_object()

        if request.method == 'GET':
            serializer = SourceSerializer(quote.source)  
            return Response(serializer.data)

        elif request.method == 'POST':
            if quote.source:  
                return Response({"error": "This quote already has a source."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = SourceSerializer(data=request.data)
            if serializer.is_valid():
                source = serializer.save()  
                quote.source = source  
                quote.save()  
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)