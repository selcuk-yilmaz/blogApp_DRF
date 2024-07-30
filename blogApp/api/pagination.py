from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import CursorPagination

class MyPageNumberPagination(PageNumberPagination):
    page_size = 3                       
    # page_size_query_param="sayfa"     


class MyLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5              
    # limit_query_param = 'how_many'  



class MycursorPagination(CursorPagination):
    page_size=10                
    ordering = "-id"           