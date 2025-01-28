from .models import User, Quote, Theme, Comment, Source, Upvote
from .serializers import (UserSerializer, QuoteSerializer,
                          ThemeSerializer, SourceSerializer,
                          QuoteListSerializer, CommentSerializer, CommentListSerializer,
                          UpvoteSerializer,UpvoteListSerializer
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

from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import User, Quote, Source, Theme, Comment, Upvote
from .serializers import (
    UserSerializer, QuoteSerializer, QuoteListSerializer,
    CommentSerializer, CommentListSerializer, UpvoteSerializer, UpvoteListSerializer,
    SourceSerializer, ThemeSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing users.

    - List all users (GET /users/)
    - Create a new user (POST /users/)
    - Retrieve a specific user (GET /users/{id}/)
    - Update a user (PUT /users/{id}/)
    - Partially update a user (PATCH /users/{id}/)
    - Delete a user (DELETE /users/{id}/)
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = ['username']
    ordering_fields = ['username', 'created_at']
    ordering = ['username']
    filterset_fields = ['username']

    @action(detail=True, methods=['get'])
    def get_all_quotes(self, request, pk=None):
        """
        Retrieve all quotes in the system.

        Accessible at GET /users/{id}/get_all_quotes/
        """
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
    """
    API endpoint for managing quotes.

    - List all quotes (GET /quotes/)
    - Create a new quote (POST /quotes/)
    - Retrieve a specific quote (GET /quotes/{id}/)
    - Update a quote (PUT /quotes/{id}/)
    - Partially update a quote (PATCH /quotes/{id}/)
    - Delete a quote (DELETE /quotes/{id}/)
    """

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
        """Return different serializers based on action (list or detail)."""
        if self.action == "list":
            return QuoteListSerializer
        return QuoteSerializer

    @action(detail=True, methods=['get', 'post'])
    def comments(self, request, pk=None):
        """
        Retrieve or add comments to a quote.

        - GET /quotes/{id}/comments/ → List all comments on the quote
        - POST /quotes/{id}/comments/ → Add a new comment to the quote
        """
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
    """
    API endpoint for managing sources.

    - GET /sources/{id}/ → Retrieve source details
    - PUT /sources/{id}/ → Fully update a source
    - PATCH /sources/{id}/ → Partially update a source
    - DELETE /sources/{id}/ → Delete a source and remove associations
    """
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
        return Response({"message": "Source deleted, and associations removed from related quotes"},
                        status=status.HTTP_204_NO_CONTENT)


class ThemeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing themes.

    - List all themes (GET /themes/)
    - Create a new theme (POST /themes/)
    - Retrieve a specific theme (GET /themes/{id}/)
    - Update a theme (PUT /themes/{id}/)
    - Partially update a theme (PATCH /themes/{id}/)
    - Delete a theme (DELETE /themes/{id}/)
    """

    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    filterset_fields = ['name']

    @action(detail=True, methods=['get'])
    def quotes(self, request, pk=None):
        """
        Retrieve all quotes under a specific theme.

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
        Retrieve the most popular themes based on the number of quotes.

        Accessible at GET /themes/popular/
        """
        try:
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
    API endpoint for managing comments.

    - List all comments (GET /comments/)
    - Create a new comment (POST /comments/)
    - Retrieve a specific comment (GET /comments/{id}/)
    - Update a comment (PUT /comments/{id}/)
    - Partially update a comment (PATCH /comments/{id}/)
    - Delete a comment (DELETE /comments/{id}/)
    """

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        """Return different serializers based on action."""
        if self.action == "list":
            return CommentListSerializer
        return CommentSerializer

    def get_object(self):
        """Retrieve a specific comment by ID."""
        comment_id = self.kwargs["pk"]
        return get_object_or_404(Comment, id=comment_id)

    def perform_create(self, serializer):
        """Automatically attach a quote to the comment when saving."""
        quote_id = self.kwargs.get("quote_id")
        quote = get_object_or_404(Quote, id=quote_id)
        serializer.save(quote=quote)


class UpvoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing upvotes on comments.

    - List all upvotes on a comment (GET /comments/{comment_id}/upvotes/)
    - Create a new upvote (POST /comments/{comment_id}/upvotes/)
    """

    serializer_class = UpvoteSerializer

    def get_serializer_class(self):
        """Return different serializers based on action."""
        if self.action == 'list':
            return UpvoteListSerializer
        return UpvoteSerializer

    def get_queryset(self):
        """Retrieve all upvotes for a specific comment."""
        return Upvote.objects.filter(comment=self.kwargs['comment_pk'])

    def perform_create(self, serializer):
        """Attach a comment to an upvote when saving."""
        comment = get_object_or_404(Comment, pk=self.kwargs['comment_pk'])
        user_id = self.request.data.get('user_id')
        serializer.save(comment=comment, user_id=user_id)
