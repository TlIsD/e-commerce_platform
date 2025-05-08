from rest_framework.pagination import PageNumberPagination

class OrderListPageNumberPagination(PageNumberPagination):
    # 订单列表分页器
    page_size = 5  # 每一页显示数据量
    page_size_query_param = "size"  # 地址栏上的页码
    max_page_size = 20  # 每页最大数据量
    page_query_param = "page" # 地址栏上的页面参数名