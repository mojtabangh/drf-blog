from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from blog.models import Article
from blog.filters import ArticleFilter


def article_detail(*, slug: str):
    return get_object_or_404(Article, slug=slug)


def article_list(*, filters=None) -> QuerySet[Article]:
    filters = filters or {}
    qs = Article.objects.all()
    return ArticleFilter(filters, qs).qs
