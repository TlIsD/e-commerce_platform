from rest_framework.pagination import PageNumberPagination


class CourseListPagination(PageNumberPagination):
    # 课程列表分页器
    page_size = 8
    max_page_size = 20
    page_size_query_param = 'size'
    page_query_param = 'page'