
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Comment, Quote
from ..serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    Handles Comments for a specific quote 
    Url structrure :/api/v1/quotes/{quote_id}/comments/
    """

    serializer_class = CommentSerializer

    def get_queryset(self):
        quote_id = self.kwargs["quote_id"]
        if quote_id:
            return Comment.objects.filter(quote_id=quote_id)
        return Comment.objects.all()

    def get_object(self):
        comment_id = self.kwargs['pk']
        return get_object_or_404(Comment, id=comment_id)

    def perform_create(self, serializer):
        quote_id = self.kwargs["quote_id"]
        if quote_id:
            quote = get_object_or_404(Quote, id=quote_id)
            serializer.save(quote=quote)
        else:
            serializer.save()