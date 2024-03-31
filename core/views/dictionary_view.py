from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.serializers import DictionarySerializer
from core.utils.dictionary import create_japanese_dict

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dictionary_view(request, term_search):
    if request.method == "GET":
        japanese_dict = create_japanese_dict()
        results = []

        for term in japanese_dict:
            if term_search in term['term'] or term_search in term['reading'] or term_search in term['translates']:
                results.append(term)

        if results:
            serializer = DictionarySerializer(results, many=True)
            data = {
                "results": serializer.data,
                "count": len(results)
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("Nenhum resultado encontrado.", status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)