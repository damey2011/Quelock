from rest_framework import pagination


class FeedsPagination(pagination.PageNumberPagination):
    page_size = 10
