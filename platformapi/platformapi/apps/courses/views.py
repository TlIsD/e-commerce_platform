from django_redis import get_redis_connection
from rest_framework.generics import ListAPIView, RetrieveAPIView
from datetime import datetime, timedelta
import constants
from .models import CourseDirection, CourseCategory, Course, CourseChapter
from .serializers import CourseDirectionSerializer, CourseCategorySerializer, CourseInfoSerializer, \
    CourseIndexHaystackSerializer, CourseRetrieveModelSerializer, CourseChapterSerializer
from rest_framework.filters import OrderingFilter
from .paginations import CourseListPagination
from drf_haystack.viewsets import HaystackViewSet
from drf_haystack.filters import HaystackFilter
from rest_framework.response import Response
from rest_framework.views import APIView


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

    def list(self, request, *args, **kwargs):
        # 保存本次搜索的关键字
        redis = get_redis_connection('hot_word')
        text = request.query_params.get('text')
        if text:
            key = f"{constants.DEFAULT_HOT_WORD}:{datetime.now().strftime('%Y:%m:%d')}"
            is_exist = redis.exists(key)
            # 搜索关键字次数加1
            redis.zincrby(key, 1, text)
            if not is_exist:
                redis.expire(key, constants.HOT_WORD_EXPIRE * 24 * 3600)

        return super().list(request, *args, **kwargs)


class HotWordAAPIView(APIView):
    # 搜索热词
    def get(self, request):
        redis = get_redis_connection("hot_word")

        date_list = []
        # 获取指定天数的热词的key
        for i in range(0, constants.HOT_WORD_EXPIRE):
            day = datetime.now() - timedelta(days=i)

            # 补0
            full_month = day.month if day.month >= 10 else f'0{day.month}'
            full_day = day.day if day.day >= 10 else f'0{day.day}'

            key = f"{constants.DEFAULT_HOT_WORD}:{day.year}:{full_month}:{full_day}"
            date_list.append(key)

        # 删除原有的统计 并统计近几天搜索词次数
        redis.delete(constants.DEFAULT_HOT_WORD)
        redis.zunionstore(constants.DEFAULT_HOT_WORD, date_list, aggregate="sum")

        # 按权重值倒序排序
        word_list = redis.zrevrange(constants.DEFAULT_HOT_WORD, 0, constants.HOT_WORD_LENGTH - 1)

        return Response(word_list)


class CourseRetrieveAPIView(RetrieveAPIView):
    # 课程详情信息
    queryset = Course.objects.filter(is_show=True, is_deleted=False).all()
    serializer_class = CourseRetrieveModelSerializer


class CourseChapterListAPIView(ListAPIView):
    # 课程章节列表
    serializer_class = CourseChapterSerializer
    def get_queryset(self):
        # 列表页数据
        course = int(self.kwargs.get("course", 0))
        try:
            ret = Course.objects.filter(pk=course).all()
        except:
            return []
        queryset = CourseChapter.objects.filter(course=course,is_show=True, is_deleted=False).order_by("order", "id")
        return queryset.all()