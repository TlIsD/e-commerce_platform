from django.conf import settings
from rest_framework import serializers
from .models import CourseDirection, CourseCategory, Course
from .search_indexes import CourseIndex
from drf_haystack.serializers import HaystackSerializer

class CourseDirectionSerializer(serializers.ModelSerializer):
    # 学习方向序列化器
    class Meta:
            model = CourseDirection
            fields = ['id', 'name']

class CourseCategorySerializer(serializers.ModelSerializer):
    # 课程分类序列化器
    class Meta:
        model = CourseCategory
        fields = ['id', 'name']

class CourseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'course_cover', 'level', 'get_level_display', 'students', 'status', 'get_status_display',
                  'lessons', 'pub_lessons', 'price', 'discount']

class CourseIndexHaystackSerializer(HaystackSerializer):
    # 课程搜索序列化器
    class Meta:
        index_classes = [CourseIndex]
        fields = ['text', 'id', 'name', 'course_cover', 'get_level_display', 'students', 'get_status_display', 'pub_lessons', 'price', 'discount', 'order']

    def to_representation(self, instance):
        """用于指定返回数据的字段"""
        # 手动拼接图片地址的域名
        instance.course_cover = f'//{settings.OSS_BUCKET_NAME}.{settings.OSS_ENDPOINT}/upload/{instance.course_cover}'
        return super().to_representation(instance)
