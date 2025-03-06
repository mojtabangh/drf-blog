from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import serializers
from drf_spectacular.utils import extend_schema

from api.mixins import ApiAuthMixin
from api.pagination import get_paginated_response, LimitOffsetPagination

from blog.models import Article
from blog.selectors.articles import article_list


class ArticleCreateApi(ApiAuthMixin, APIView):
    ...


class ArticleDetailApi(APIView):
    ...


class ArticleListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 20

    class ArticleFilterSerializer(serializers.Serializer):
        search = serializers.CharField(required=False, max_length=100)

    class ArticleOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = ("title", "slug", "content", "author")

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

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.ArticleOutputSerializer,
            queryset=query,
            request=request,
            view=self,
        )
