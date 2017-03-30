from rest_framework.pagination import CursorPagination


class TopicAnswersPagination(CursorPagination):
    page_size = 1
    ordering = ['date_written', 'time_written']


class TopicPagination(CursorPagination):
    page_size = 2


class CommonUserPagination(CursorPagination):
    page_size = 1
    ordering = 'id'