from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import CourseDirection, CourseCategory, Course
from .serializers import CourseDirectionSerializer, CourseCategorySerializer, CourseInfoSerializer


# Create your views here.
class CourseDirectionListAPIView(ListAPIView):
    # 学习方向
    queryset = CourseDirection.objects.filter(is_show=True, is_deleted=False).order_by('order', '-id')
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

        return queryset.order_by('order', '-id').all()


class CourseListAPIView(ListAPIView):
    # 课程列表信息
    serializer_class = CourseInfoSerializer

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