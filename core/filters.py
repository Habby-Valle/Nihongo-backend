from django.db.models import Q
from django_filters import rest_framework as filters

from core.models import Grammar, Text, Word


class GrammarFilter(filters.FilterSet):
    grammar = filters.CharFilter(field_name="grammar", lookup_expr="icontains")
    structure = filters.CharFilter(field_name="structure", lookup_expr="icontains")
    level = filters.NumberFilter(field_name="level")
    search = filters.CharFilter(method="custom_search")

    class Meta:
        model = Grammar
        fields = ["grammar", "structure", "level"]

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            Q(grammar__icontains=value)
            | Q(structure__icontains=value)
            | Q(level__icontains=value)
        )


class WordFilter(filters.FilterSet):
    word = filters.CharFilter(field_name="word", lookup_expr="icontains")
    meaning = filters.CharFilter(field_name="meaning", lookup_expr="icontains")
    reading = filters.CharFilter(field_name="reading", lookup_expr="icontains")
    level = filters.NumberFilter(field_name="level")
    type = filters.CharFilter(field_name="type", lookup_expr="icontains")
    category = filters.CharFilter(field_name="category__name", lookup_expr="icontains")
    search = filters.CharFilter(method="custom_search")

    class Meta:
        model = Word
        fields = ["word", "meaning", "reading"]

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            Q(word__icontains=value)
            | Q(meaning__icontains=value)
            | Q(reading__icontains=value)
            | Q(level__icontains=value)
            | Q(type__icontains=value)
            | Q(category__name__icontains=value)
        )


class TextFilter(filters.FilterSet):
    class Meta:
        model = Text
        fields = {
            "title": ["exact", "icontains"],
        }
