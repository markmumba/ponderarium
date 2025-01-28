from .models import User, Quote, Theme, Comment, Source, Upvote
from .serializers import (UserSerializer, QuoteSerializer,
                          ThemeSerializer, SourceSerializer,
                          QuoteListSerializer, CommentSerializer, CommentListSerializer,
                          UpvoteSerializer
                          )


from rest_framework import viewsets
from django.db.models import Count
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
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

    @action(['get'], detail=True)
    def get_all_quotes(self, request, pk=None):
        try:
            user = self.get_object()
            quotes = Quote.objects.all()
            serializer = QuoteSerializer(quotes, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
            serializer = CommentListSerializer(comments, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(quote=quote)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def source_detail(request, pk):
    source = get_object_or_404(Source, pk=pk)

    if request.method == 'GET':
        serializer = SourceSerializer(source)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = SourceSerializer(
            source, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        quotes_with_source = Quote.objects.filter(source=source)
        for quote in quotes_with_source:
            quote.source = None
            quote.save()

        source.delete()
        return Response({"message": "Source delete and association removed from related quotes"}, status=status.HTTP_204_NO_CONTENT)


class ThemeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Theme objects.

    Provides CRUD operations and additional functionality for themes:
    - List all themes (GET /themes/)
    - Create new theme (POST /themes/)
    - Retrieve single theme (GET /themes/{id}/)
    - Update theme (PUT /themes/{id}/)
    - Partially update theme (PATCH /themes/{id}/)
    - Delete theme (DELETE /themes/{id}/)
    """

    # Basic configuration
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer

    # Add filtering and searching capabilities
    filter_backends = [
        DjangoFilterBackend,  # For exact matching filters
        filters.SearchFilter,  # For text search
        filters.OrderingFilter  # For sorting
    ]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    filterset_fields = ['name']

    @action(detail=True, methods=['get'])
    def quotes(self, request, pk=None):
        """
        Custom endpoint to get quotes for a specific theme.
        Accessible at GET /themes/{id}/quotes/
        """
        try:
            theme = self.get_object()
            quotes = theme.quotes.all()
            serializer = QuoteSerializer(quotes, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def popular(self, request):
        """
        Custom endpoint to get popular themes.
        Accessible at GET /themes/popular/
        """
        try:
            # Get themes with the most quotes
            popular_themes = Theme.objects.annotate(
                quote_count=Count('quotes')
            ).order_by('-quote_count')[:5]

            serializer = self.get_serializer(popular_themes, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CommentViewSet(viewsets.ModelViewSet):
    """
    Handles Comments for a specific quote 
    URL structure: /api/v1/quotes/{quote_id}/comments/
    """

    serializer_class = CommentSerializer
    queryset=Comment.objects.all()

    def get_serializer_class(self):
        print(f"Current action: {self.action} ")
        if self.action == "list":
            return CommentListSerializer
        return CommentSerializer


    def get_object(self):
        comment_id = self.kwargs["pk"]
        return get_object_or_404(Comment, id=comment_id)

    def perform_create(self, serializer):
        """Automatically attach quote to the comment when saving"""
        quote_id = self.kwargs.get("quote_id")
        quote = get_object_or_404(Quote, id=quote_id)

        serializer.save(quote=quote)


class UpvoteViewSet(viewsets.ModelViewSet):
    serializer_class = UpvoteSerializer
    
    def get_queryset(self):
        # Changed from comment_id to comment
        return Upvote.objects.filter(comment=self.kwargs['comment_pk'])
    
    def perform_create(self, serializer):
        comment = Comment.objects.get(pk=self.kwargs['comment_pk'])
        user_id = self.request.data.get('user_id')
        serializer.save(
            comment=comment,
            user_id=user_id
        )