from django.shortcuts import render
from rest_framework.response import Response
from rest_framework  import viewsets
from django.db.models import Count


from ..models import Theme
from ..serializers import  ThemeSerializer,QuoteSerializer

from rest_framework import status


from rest_framework import viewsets, status
from rest_framework.response import Response
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




