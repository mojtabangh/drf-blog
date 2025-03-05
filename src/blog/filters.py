from django_filters import (
    FilterSet,
    CharFilter
)
from django.contrib.postgres.search import SearchVector

from .models import Article


class ArticleFilter(FilterSet):
    search = CharFilter(method="filter_search")

    def filter_search(self, queryset, name, value):
        return queryset.annotate(search=SearchVector("title")).filter(search=value)

    class Meta:
        model = Article
        fields = ("title",)
