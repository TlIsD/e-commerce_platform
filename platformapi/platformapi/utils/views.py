from rest_framework.generics import ListAPIView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from constants import LIST_CACHE_PAGE_TIME


class CachedListAPIView(ListAPIView):
    # 列表缓存视图
    @method_decorator(cache_page(LIST_CACHE_PAGE_TIME))
    def get(self, request, *args, **kwargs):
        # 装饰ListAPIView的get方法
        return super().get(request, *args, **kwargs)