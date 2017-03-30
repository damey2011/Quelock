from rest_framework.pagination import CursorPagination, PageNumberPagination


class UserAnswerPagination(CursorPagination):
    page_size = 2
    ordering = ['date_written', 'time_written']


class TrendingAnswersPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100
