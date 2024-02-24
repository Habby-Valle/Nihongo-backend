from django_filters import rest_framework as filters

from core.models import Grammar, Text, Word
from django.db.models import Q

class GrammarFilter(filters.FilterSet):
    class Meta:
        model = Grammar
        fields = {
            "grammar": ["exact", "icontains"],
            "structure": ["exact", "icontains"],
            "level": ["exact"],
        }

class WordFilter(filters.FilterSet):
    word = filters.CharFilter(field_name='word', lookup_expr='icontains')
    meaning = filters.CharFilter(field_name='meaning', lookup_expr='icontains')
    reading = filters.CharFilter(field_name='reading', lookup_expr='icontains')
    search = filters.CharFilter(method='custom_search')

    class Meta:
        model = Word
        fields = ['word', 'meaning', 'reading']

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            Q(word__icontains=value) | 
            Q(meaning__icontains=value) | 
            Q(reading__icontains=value)
        )

class TextFilter(filters.FilterSet):
    class Meta:
        model = Text
        fields = {
            "title": ["exact", "icontains"],
        }
