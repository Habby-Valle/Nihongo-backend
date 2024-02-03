import django_filters

from core.models import Grammar, Text, Word


class GrammarFilter(django_filters.FilterSet):
    class Meta:
        model = Grammar
        fields = {
            "grammar": ["exact", "icontains"],
            "structure": ["exact", "icontains"],
            "level": ["exact"],
        }


class WordFilter(django_filters.FilterSet):
    class Meta:
        model = Word
        fields = {
            "word": ["exact", "icontains"],
            "meaning": ["exact", "icontains"],
            "level": ["exact"],
        }


class TextFilter(django_filters.FilterSet):
    class Meta:
        model = Text
        fields = {
            "title": ["exact", "icontains"],
        }
