from rest_framework import pagination

class StandartResutlsSetPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page-size'