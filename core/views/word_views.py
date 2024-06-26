import random

from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.filters import WordFilter
from core.models import Word
from core.serializers import WordCreateSerializer, WordSerializer
from core.utils.paginationn import CustomPagination


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def word_list(request):
    if request.method == "GET":
        words = Word.objects.filter(created_by=request.user)
        words_ordered = words.order_by("-created_at")
        filter = WordFilter(request.GET, queryset=words_ordered)
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(filter.qs, request)
        serializer = WordSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
    elif request.method == "POST":
        serializer = WordCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)

            data = {"message": "Word created successfully", "word": serializer.data}
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def word_detail(request, pk):
    try:
        word = Word.objects.get(pk=pk)
    except Word.DoesNotExist:
        return Response({"message": "Word not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = WordSerializer(word)
        data = {"word": serializer.data}

        return Response(data)
    elif request.method == "PATCH":
        serializer = WordCreateSerializer(word, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            data = {"message": "Word updated successfully", "word": serializer.data}

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        word.delete()
        return Response(
            {"message": "Word deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def word_today_view(request):
    word_data = None
    if request.method == "GET":
        if "word_of_the_day_id" in request.session:
            word_id = request.session["word_of_the_day_id"]
            word_today = Word.objects.get(pk=word_id)
        else:
            words = Word.objects.filter(created_by=request.user)
            if words.count() > 0:
                word_today = random.choice(words)
                request.session["word_of_the_day_id"] = word_today.id

                end_of_day = timezone.localtime()
                end_of_day = end_of_day.replace(hour=23, minute=59, second=59)
                request.session.set_expiry(end_of_day)
            else:
                word_today = None

        if word_today:
            serializer = WordSerializer(word_today)
            word_data = serializer.data

        data = {"word_today": word_data}

        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
