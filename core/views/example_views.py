from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Example, Word
from core.serializers import ExampleCreateSerializer, ExampleSerializer
from core.utils.paginationn import CustomPagination


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def example_list(request, word_id):
    try:
        word = Word.objects.get(pk=word_id)
    except Word.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        examples = Example.objects.filter(created_by=request.user, word=word)

        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(examples, request)
        serializer = ExampleSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
    elif request.method == "POST":
        serializer = ExampleCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(created_by=request.user, word=word)

            data = {
                "message": "Example created successfully",
                "example": serializer.data,
            }

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def example_detail(request, word_id, example_id):
    try:
        word = Word.objects.get(pk=word_id)
    except Word.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        example = Example.objects.get(pk=example_id, word=word)
    except Example.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ExampleSerializer(example)

        data = {"example": serializer.data}

        return Response(data)

    elif request.method == "PATCH":
        serializer = ExampleCreateSerializer(example, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            data = {
                "message": "Example updated successfully",
                "example": serializer.data,
            }

            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        example.delete()

        data = {"message": "Example deleted successfully"}

        return Response(data, status=status.HTTP_204_NO_CONTENT)
