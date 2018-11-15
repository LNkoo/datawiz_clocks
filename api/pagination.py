from rest_framework.pagination import (
    LimitOffsetPagination, PageNumberPagination
)


class PostLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 12
    max_limit = 12


class PostPageNumberPagination(PageNumberPagination):
    page_size = 2
