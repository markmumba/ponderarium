from django.core.serializers import serialize
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from django.db.models import Count
from ..models import Source
from ..serializers import SourceSerializer


@api_view(['GET', 'POST'])
def source_list(request):
    """
    Handles the get request and the post request for the sources
    """
    if request.method == 'GET':
        sources = Source.objects.all()
        serializer = SourceSerializer(sources, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = SourceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def source_detail(request, pk):
    """
    Handles retrieving ,updating and deleting sources
    """
    try:
        source = Source.objects.get(pk=pk)
    except Source.DoesNotExist:
        return Response({"error":"Source not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SourceSerializer(source)
        return Response(serializer.data)


    elif request.method in ['PUT','PATCH']:
        serializer = SourceSerializer(source , data=request.data,partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        source.delete()
        return Response({"message":"Source deleted"}, status= status.HTTP_204_NO_CONTENT)