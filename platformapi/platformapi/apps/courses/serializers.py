from rest_framework import serializers
from .models import CourseDirection, CourseCategory


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