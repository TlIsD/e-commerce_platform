from django.conf import settings
from rest_framework import serializers
from .models import CourseDirection, CourseCategory, Course, Teacher, CourseChapter
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


class CourseTeacherSerializer(serializers.ModelSerializer):
    # 课程教师信息
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'avatar', 'role', 'get_role_display', 'title', 'signature', 'brief']


class CourseRetrieveModelSerializer(serializers.ModelSerializer):
    # 课程详情的序列化器
    direction_name = serializers.CharField(source="direction.name")
    category_name = serializers.CharField(source="category.name")

    # 序列化器嵌套
    teacher = CourseTeacherSerializer()

    class Meta:
        model = Course
        fields = [
            "name", "course_cover", "course_video", "level", "get_level_display",
            "description", "pub_date", "status", "get_status_display", "students","discount",
            "lessons", "pub_lessons", "price", "direction", "direction_name", "category", "category_name", "teacher"
        ]


class CourseChapterSerializer(serializers.ModelSerializer):
    # 课程章节序列化器
    class Meta:
        model = CourseChapter
        fields = ["id", "orders", "name", "summary", "get_lesson_list"]