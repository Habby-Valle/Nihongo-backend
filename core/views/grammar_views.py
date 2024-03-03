from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.filters import GrammarFilter
from core.models import Grammar
from core.serializers import GrammarCreateSerializer, GrammarSerializer
from core.utils.paginationn import CustomPagination


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def grammar_list(request):
    if request.method == "GET":
        grammars = Grammar.objects.filter(created_by=request.user).order_by("-created_at")
        filter = GrammarFilter(request.GET, queryset=grammars)
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(filter.qs, request)
        serializer = GrammarSerializer(instance=result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
    elif request.method == "POST":
        serializer = GrammarCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(created_by=request.user)

            data = {"message": "Grammar created", "grammar": serializer.data}

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def grammar_detail(request, pk):
    try:
        grammar = Grammar.objects.get(pk=pk)
    except Grammar.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = GrammarSerializer(grammar)

        data = {"grammar": serializer.data}

        return Response(data)

    elif request.method == "PUT":
        serializer = GrammarCreateSerializer(grammar, data=request.data)

        if serializer.is_valid():
            serializer.save()

            data = {"message": "Grammar updated", "grammar": serializer.data}

            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PATCH":
        serializer = GrammarCreateSerializer(grammar, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            data = {"message": "Grammar updated", "grammar": serializer.data}

            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        grammar.delete()

        data = {"message": "grammar deleted"}
        return Response(data, status=status.HTTP_204_NO_CONTENT)
