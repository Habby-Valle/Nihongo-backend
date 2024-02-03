from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.filters import TextFilter
from core.models import Text
from core.serializers import TextCreateSerializer, TextSerializer
from core.utils.paginationn import CustomPagination


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def text_list(request):
    if request.method == "GET":
        texts = Text.objects.filter(created_by=request.user)
        filter = TextFilter(request.GET, queryset=texts)
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(filter.qs, request)
        serializer = TextSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

    elif request.method == "POST":
        serializer = TextCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(created_by=request.user)

            data = {"message": "Text created successfully", "text": serializer.data}

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def text_detail(request, text_id):
    try:
        text = Text.objects.get(pk=text_id)
    except Text.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = TextSerializer(text)

        data = {"text": serializer.data}

        return Response(data)
    elif request.method == "PATCH":
        serializer = TextCreateSerializer(text, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            data = {"message": "Text updated successfully", "text": serializer.data}

            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        text.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
