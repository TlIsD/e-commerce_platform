from rest_framework import serializers
from .models import CourseDirection

class CourseDirectionSerializer(serializers.ModelSerializer):
    # 学习方向序列化器
    class Meta:
            model = CourseDirection
            fields = ['id', 'name']