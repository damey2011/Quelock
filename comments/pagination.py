from rest_framework.pagination import PageNumberPagination


class CommentsPagination(PageNumberPagination):
    page_size = 5