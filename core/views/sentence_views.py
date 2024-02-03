from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Sentence
from core.serializers import SentenceCreateSerializer, SentenceListSerializer
from core.utils.paginationn import CustomPagination


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def sentences_list(request, grammar_id):
    try:
        sentences = Sentence.objects.filter(
            grammar_id=grammar_id, created_by=request.user
        )
    except Sentence.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(sentences, request)
        serializer = SentenceListSerializer(instance=result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
    elif request.method == "POST":
        serializer = SentenceCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(created_by=request.user)

            data = {"message": "Sentence created", "sentence": serializer.data}

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def sentence_detail(request, pk):
    try:
        sentence = Sentence.objects.get(pk=pk)
    except Sentence.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = SentenceListSerializer(sentence)

        data = {"sentence": serializer.data}

        return Response(data)

    elif request.method == "PATCH":
        serializer = SentenceCreateSerializer(sentence, data=request.data)

        if serializer.is_valid():
            serializer.save()

            data = {"message": "Sentence updated", "sentence": serializer.data}

            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        sentence.delete()

        data = {"message": "Sentence deleted"}

        return Response(data, status=status.HTTP_204_NO_CONTENT)
