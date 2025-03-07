from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import serializers
from drf_spectacular.utils import extend_schema

from api.mixins import ApiAuthMixin
from api.pagination import get_paginated_response_context, LimitOffsetPagination

from blog.models import Article
from blog.selectors.articles import article_list, article_detail
from blog.services.articles import create_article


class ArticleApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 20

    class ArticleCreateSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=150, required=True,)
        content = serializers.CharField(max_length=20_000, required=True)

    class ArticleOutputSerializer(serializers.ModelSerializer):
        url = serializers.SerializerMethodField("get_url")
        author = serializers.SerializerMethodField("get_author_email")

        class Meta:
            model = Article
            fields = ("title", "author", "url",)

        def get_url(self, article):
            request = self.context.get("request")
            path = reverse("api:blog:article-detail", args=(article.slug,))
            return request.build_absolute_uri(path)

        def get_author_email(self, article):
            return article.author.email

    class ArticleFilterSerializer(serializers.Serializer):
        search = serializers.CharField(required=False, max_length=100)
        created_at__range = serializers.CharField(
            required=False,
            max_length=30,
            help_text="enter two ranges. example: \"2025-03-05,2025-03-08\" or \"2025-03-05,\" or \",2025-03-05\" ",
        )

    @extend_schema(request=ArticleCreateSerializer, responses=ArticleOutputSerializer)
    def post(self, request):
        serializer = self.ArticleCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            query = create_article(
                title=serializer.validated_data.get("title"),
                content=serializer.validated_data.get("content"),
                author=request.user
            )
        except Exception as ex:
            return Response(
                {"detail": f"Database Error - {ex}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            self.ArticleOutputSerializer(query, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        parameters=[ArticleFilterSerializer],
        responses=ArticleOutputSerializer
    )
    def get(self, request):
        filter_serializer = self.ArticleFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        try:
            query = article_list(filters=filter_serializer.validated_data)
        except Exception as ex:
            return Response(
                {"detail": f"Filter Error - {ex}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.ArticleOutputSerializer,
            queryset=query,
            request=request,
            view=self,
        )


class ArticleDetailApi(APIView):
    class ArticleDetailSerializer(serializers.ModelSerializer):
        author = serializers.SerializerMethodField("get_author_email")

        class Meta:
            model = Article
            fields = ("title", "content", "author")

        def get_author_email(self, article):
            return article.author.email

    @extend_schema(responses=ArticleDetailSerializer,)
    def get(self, request, slug):
        try:
            query = article_detail(slug=slug)
        except Exception as ex:
            return Response(
                {"detail": f"Article not found - {ex}"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.ArticleDetailSerializer(query)
        return Response(serializer.data,)
