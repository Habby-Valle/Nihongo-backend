from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import TextWriting
from core.serializers import TextWritingCreateSerializer, TextWritingSerializer
from core.utils.paginationn import CustomPagination


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def text_writing_list(request):
    if request.method == "GET":
        text_writings = TextWriting.objects.filter(created_by=request.user).order_by("-created_at")

        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(text_writings, request)
        serializer = TextWritingSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

    elif request.method == "POST":
        serializer = TextWritingCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(created_by=request.user)

            data = {
                "message": "Text Writing created successfully",
                "text_writing": serializer.data,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def text_writing_detail(request, text_writing_id):
    try:
        text_writing = TextWriting.objects.get(pk=text_writing_id)
    except TextWriting.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = TextWritingSerializer(text_writing)

        data = {"text_writing": serializer.data}

        return Response(data)

    elif request.method == "PATCH":
        serializer = TextWritingSerializer(
            text_writing, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()

            data = {
                "message": "Text Writing updated successfully",
                "text_writing": serializer.data,
            }
            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        text_writing.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
