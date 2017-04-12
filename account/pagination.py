from rest_framework.pagination import CursorPagination


class FollowPagination(CursorPagination):
    page_size = 15

class UserOtherDetailsPagination(CursorPagination):
    page_size = 15
    ordering = '-no_of_answers'