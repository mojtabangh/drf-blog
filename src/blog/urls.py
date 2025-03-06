from django.urls import path

from .apis import (
    ArticleListApi,
    ArticleCreateApi,
    ArticleDetailApi
)

app_name = "blog"

urlpatterns = [
    path("articles/", ArticleListApi.as_view(), name="article-list"),
    path("articles/", ArticleCreateApi.as_view(), name="article-create"),
    path("article/<slug:slug>/", ArticleDetailApi.as_view(), name="article-detail"),
]
