from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import CourseDirection, CourseCategory, Course
from .serializers import CourseDirectionSerializer, CourseCategorySerializer, CourseInfoSerializer, CourseIndexHaystackSerializer
from rest_framework.filters import OrderingFilter
from .paginations import CourseListPagination
from drf_haystack.viewsets import HaystackViewSet
from drf_haystack.filters import HaystackFilter


# Create your views here.
class CourseDirectionListAPIView(ListAPIView):
    # 学习方向
    queryset = CourseDirection.objects.filter(is_show=True, is_deleted=False).order_by('order', 'id')
    serializer_class = CourseDirectionSerializer
    pagination_class = None


class CourseCategoryListAPIView(ListAPIView):
    # 学习分类
    serializer_class = CourseCategorySerializer
    pagination_class = None

    def get_queryset(self):
        # 获取路由参数
        queryset = CourseCategory.objects.filter(is_show=True, is_deleted=False)

        direction = int(self.kwargs.get('direction', 0))
        if direction > 0:
            queryset = queryset.filter(direction=direction)

        return queryset.order_by('order', 'id').all()


class CourseListAPIView(ListAPIView):
    # 课程列表信息
    serializer_class = CourseInfoSerializer
    filter_backends = [OrderingFilter, ]
    ordering_fields = ['id', 'students', 'order']
    pagination_class = CourseListPagination

    def get_queryset(self):
        # 列表页数据
        direction = int(self.kwargs.get('direction', 0))
        category = int(self.kwargs.get('category', 0))

        queryset = Course.objects.filter(is_show=True, is_deleted=False).order_by('-order', '-id')
        if direction > 0:
            # 只有学习方向才进行学习方向的过滤
            queryset = queryset.filter(direction=direction)

        if category > 0:
            # 课程分类过滤
            queryset = queryset.filter(category=category)

        return queryset.all()


class CourseSearchView(HaystackViewSet):
    # 课程搜索视图类
    # 指定本次搜索最终真实数据的保存模型
    index_model = [Course]
    serializer_class = CourseIndexHaystackSerializer
    filter_backends = [OrderingFilter, HaystackFilter]
    ordering_fields = ['id', 'students', 'order']
    pagination_class = CourseListPagination