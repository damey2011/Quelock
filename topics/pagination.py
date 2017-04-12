from rest_framework.pagination import CursorPagination


class TopicAnswersPagination(CursorPagination):
    page_size = 15
    ordering = ['time_written']


class TopicPagination(CursorPagination):
    page_size = 15


class CommonUserPagination(CursorPagination):
    page_size = 10
    ordering = 'id'