from django_filters import (
    FilterSet,
    CharFilter
)
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank
    )

from .models import Article


class ArticleFilter(FilterSet):
    search = CharFilter(method="filter_search")

    def filter_search(self, queryset, name, value):
        search_vector = SearchVector("title", "content", "slug",)
        search_query = SearchQuery(value)
        search_rank = SearchRank(search_vector, search_query)
        return queryset.annotate(rank=search_rank,).filter(rank__gt=0).order_by("-rank")

    class Meta:
        model = Article
        fields = ("title",)
