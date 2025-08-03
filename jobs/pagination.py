from rest_framework.pagination import PageNumberPagination

class JobPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'size'  # Allow ?size=5
    max_page_size = 20