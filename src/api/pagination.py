from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination as _LimitOffsetPagination
from rest_framework.serializers import Serializer


def get_paginated_response(*, pagination_class, serializer_class, queryset, request, view):
    paginator = pagination_class()

    page = paginator.paginate_queryset(queryset, request, view=view)

    serializer = serializer_class(page, many=True)
    return paginator.get_paginated_response(serializer.data)


def get_paginated_response_context(*, pagination_class, serializer_class, queryset, request, view):
    paginator = pagination_class()

    page = paginator.paginate_queryset(queryset, request, view=view)

    serializer = serializer_class(page, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)


class LimitOffsetPagination(_LimitOffsetPagination):
    default_limit = 10
    max_limit = 50

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("limit", self.limit),
                    ("offset", self.offset),
                    ("count", self.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )
