from django.shortcuts import render
from rest_framework.response import Response
from rest_framework  import viewsets
from django.db.models import Count


from ..models import User,Theme,Source,Quote,Comment,Upvote
from ..serializers import UserSerializer, ThemeSerializer,SourceSerializer,QuoteSerializer,CommentSerializer,UpvoteSerializer

from rest_framework import status


from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

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
    
    def list(self, request, *args, **kwargs):
        """
        Get all themes with error handling.
        Equivalent to your GET in the function view.
        """
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def create(self, request, *args, **kwargs):
        """
        Create a new theme with error handling.
        Equivalent to your POST in the function view.
        """
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_ERROR
            )
    
    def retrieve(self, request, *args, **kwargs):
        """Get a single theme by ID."""
        try:
            return super().retrieve(request, *args, **kwargs)
        except Theme.DoesNotExist:
            return Response(
                {"error": "Theme not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
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




