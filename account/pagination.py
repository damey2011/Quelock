from rest_framework.pagination import CursorPagination


class FollowPagination(CursorPagination):
    page_size = 2

class UserOtherDetailsPagination(CursorPagination):
    page_size = 1
    ordering = '-no_of_answers'