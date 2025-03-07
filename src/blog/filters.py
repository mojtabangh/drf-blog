from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank
    )
from django.utils import timezone
from rest_framework.exceptions import APIException
from django_filters import (
    FilterSet,
    CharFilter
)

from blog.models import Article


class ArticleFilter(FilterSet):
    search = CharFilter(method="filter_search")
    created_at__range = CharFilter(method="filter_created_at__range",)

    def filter_search(self, queryset, name, value):
        search_vector = SearchVector("title", "content", "slug",)
        search_query = SearchQuery(value)
        search_rank = SearchRank(search_vector, search_query)
        return queryset.annotate(rank=search_rank,).filter(rank__gt=0).order_by("-rank")

    def filter_created_at__range(self, queryset, name, value):
        limit = 2
        created_at__in = value.split(",")

        if len(created_at__in) > limit:
            raise APIException("enter two dates with \",\" in the middle.")

        start, end = created_at__in

        if not end:
            end = timezone.now()

        if not start:
            return queryset.filter(created_at__date__lt=end)

        return queryset.filter(created_at__range=(start, end))

    class Meta:
        model = Article
        fields = ("title",)
