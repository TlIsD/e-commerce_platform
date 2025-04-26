from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import CourseDirection
from .serializers import CourseDirectionSerializer

# Create your views here.
class CourseDirectionListAPIView(ListAPIView):
    # 学习方向
    queryset = CourseDirection.objects.filter(is_show=True, is_deleted=False).order_by('order', '-id')
    serializer_class = CourseDirectionSerializer