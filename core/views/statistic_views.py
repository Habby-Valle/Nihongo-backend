from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from core.models import Grammar, Word, Category
from rest_framework.permissions import IsAuthenticated
from core.serializers import StatisticWordByCategorySerializer, StatisticWordByLevelSerializer, StatisticGrammarByCategorySerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def statistic_view(request):
    if request.method == "GET":
        levels = ["N5", "N4", "N3", "N2", "N1", "Unknown"]
        categories = Category.objects.all()
        grammar_by_level = []
        words_by_level = []
        words_by_category = []

        for level in levels:
            grammars = Grammar.objects.filter(level=level)
            words = Word.objects.filter(level=level)

            grammar_by_level.append({
                'level_name': level,
                'grammars_count': grammars.count()
            })

            words_by_level.append({
                'level_name': level,
                'words_count': words.count()
            })

        for category in categories:
            words = Word.objects.filter(category=category)
            words_by_category.append({
                'category_name': category.name,
                'words_count': words.count()
            })
            
        serializer_grammar = StatisticGrammarByCategorySerializer(grammar_by_level, many=True)
        serializer_word = StatisticWordByLevelSerializer(words_by_level, many=True)
        serializer_word_by_category = StatisticWordByCategorySerializer(words_by_category, many=True)

        data = {
            "grammar_by_level": serializer_grammar.data,
            "words_by_level": serializer_word.data,
            "words_by_category": serializer_word_by_category.data
        }
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)