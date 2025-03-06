from django.urls import path

from .apis import (
    ArticleDetailApi,
    ArticleApi,
)

app_name = "blog"

urlpatterns = [
    path("articles/", ArticleApi.as_view(), name="article-create"),
    path("article/<slug:slug>/", ArticleDetailApi.as_view(), name="article-detail"),
]
