from rest_framework.pagination import PageNumberPagination, CursorPagination


class MyTestPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserQuestionPagination(CursorPagination):
    page_size = 2
    ordering = ['-date_asked', '-time_asked']


class ExploreQuestionPagination(CursorPagination):
    page_size = 2
    ordering = ['-date_asked', '-time_asked']
