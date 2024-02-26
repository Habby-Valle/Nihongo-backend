from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Word, Grammar, Example, Sentence, Text, TextWriting
from core.serializers import WordSerializer, GrammarSerializer, ExampleSerializer, SentenceListSerializer, TextSerializer, TextWritingSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def latest_activity(request):
    if request.method != "GET":
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    words = Word.objects.filter(created_by=request.user).order_by("-created_at")[:2]
    grammars = Grammar.objects.filter(created_by=request.user).order_by("-created_at")[:5]
    examples = Example.objects.filter(created_by=request.user).order_by("-created_at")[:5]
    sentences = Sentence.objects.filter(created_by=request.user).order_by("-created_at")[:5]
    texts = Text.objects.filter(created_by=request.user).order_by("-created_at")[:5]
    text_writings = TextWriting.objects.filter(created_by=request.user).order_by("-created_at")[:5]

    serializer_words = WordSerializer(words, many=True)
    serializer_grammars = GrammarSerializer(grammars, many=True)
    serializer_examples = ExampleSerializer(examples, many=True)
    serializer_sentences = SentenceListSerializer(sentences, many=True)
    serializer_texts = TextSerializer(texts, many=True)
    serializer_text_writings = TextWritingSerializer(text_writings, many=True)

    data_latest = [
        {"type": "palavras", "data": serializer_words.data},
        {"type": "gramáticas", "data": serializer_grammars.data},
        {"type": "exemplos", "data": serializer_examples.data},
        {"type": "sentenças", "data": serializer_sentences.data},
        {"type": "textos", "data": serializer_texts.data},
        {"type": "redações", "data": serializer_text_writings.data},
    ]

    data = {
        "latest_activity": data_latest
    }

    return Response(data, status=status.HTTP_200_OK)