from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Source,Quote
from ..serializers import SourceSerializer


@api_view(['GET','PUT','PATCH','DELETE'])
def source_detail(request,pk):
    source = get_object_or_404(Source, pk=pk)

    if request.method == 'GET':
        serializer = SourceSerializer(source)
        return Response(serializer.data)


    elif request.method in ['PUT','PATCH']:
        serializer = SourceSerializer(source,data=request.data,partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        quotes_with_source= Quote.objects.filter(source=source)
        for quote in quotes_with_source:
            quote.source = None
            quote.save()
        
        source.delete()
        return Response({"message": "Source delete and association removed from related quotes"},status=status.HTTP_204_NO_CONTENT)