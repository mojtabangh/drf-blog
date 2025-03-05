from django.urls import path

from .apis import ArticleListApi

app_name = "blog"

urlpatterns = [
    path("articles/", ArticleListApi.as_view(), name="article-list"),
]
