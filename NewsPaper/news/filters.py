from .models import Category
from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter
from django.forms import DateInput


class PostFilter(FilterSet):
    title = CharFilter(lookup_expr='iregex', label='Заголовок')
    categories = ModelChoiceFilter(label='Категория', empty_label='Любая', queryset=Category.objects.all())
    created = DateFilter(
        lookup_expr='gt',
        label='Дата после',
        widget=DateInput(attrs={'type': 'date'}),
    )