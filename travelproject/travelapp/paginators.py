from rest_framework import pagination


class TourPaginator(pagination.PageNumberPagination):
    page_size = 20
    page_query_param = 'page'


class TagPaginator(pagination.PageNumberPagination):
    page_size = 10
    page_query_param = 'page'

class NewsPaginator(pagination.PageNumberPagination):
    page_size = 4
    page_query_param = 'page'

class AttractionPaginator(pagination.PageNumberPagination):
    page_size = 10
    page_query_param = 'page'