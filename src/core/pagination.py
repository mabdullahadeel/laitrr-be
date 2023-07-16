from rest_framework.pagination import LimitOffsetPagination
from .response import Response


class WrappedLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 50
    max_limit = 100

    def get_paginated_response_schema(self, schema):
        return Response.get_response_schema(
            super().get_paginated_response_schema(schema)
        )
