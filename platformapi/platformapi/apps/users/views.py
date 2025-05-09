import random
from django.conf import settings

from courses.models import Course, CourseLesson
from .tasks import send_sms
from django_redis import get_redis_connection
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework.permissions import IsAuthenticated
from .models import User, UserCourse, StudyProgress
from platformapi.utils.tencentcloudapi import TencentCloudApi, TencentCloudSDKException
from rest_framework.response import Response
from rest_framework import status
from courses.paginations import CourseListPagination
from .serializers import UserRegisterSerializer, UserCourseModelSerializer
import constants
from django.db import transaction

import logging
logger = logging.getLogger("django")

# Create your views here.
class LoginAPIView(ObtainJSONWebToken):
    # 登录视图
    def post(self, request, *args, **kwargs):
        try:
            api = TencentCloudApi()

            result = api.captcha(
                request.data.get("ticket"),
                request.data.get("randstr"),
                # 客户端IP
                request.META.get("REMOTE_ADDR"),
            )

            if result:
                # 验证通过，调用父类登录视图方法
                return super().post(request, *args, **kwargs)
            else:
                raise TencentCloudSDKException

        except TencentCloudSDKException as err:
            return Response({"errmsg": "验证码校验失败！"}, status=status.HTTP_400_BAD_REQUEST)


# class PhoneLoginAPIView(RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserLoginSerializer
#     lookup_field = 'phone'


class PhoneAPIView(APIView):
    # ajax校验手机号是否注册
    def get(self, request, phone):
        try:
            User.objects.get(phone=phone)
            return Response({'err': '当前手机号已被注册'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'msg': 'OK'}, status=status.HTTP_200_OK)


class UserAPIView(CreateAPIView):
    # 用户注册视图
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class SmsCodeAPIView(APIView):
    def get(self, request, phone):
        # 发送短信
        redis = get_redis_connection('sms_code')

        # 判断是否发送处于冷却中
        interval = redis.ttl(f'interval_{phone}')
        if interval != -2:
            return Response({'err': f'点击过于频繁，请{interval}后点击', 'interval': interval}, status=status.HTTP_400_BAD_REQUEST)

        # 随机生成短信验证码
        captcha = f'{random.randint(0, 9999):04d}'
        # 短信有效期
        time = settings.RONGLIANYUN.get('sms_expire')
        # 短信间隔时间
        sms_interval = settings.RONGLIANYUN.get('sms_interval')
        # 调用第三方sdk发送短信
        # send_sms(settings.RONGLIANYUN.get('reg_tid'), phone, datas=(captcha, time // 60))
        # 异步发送短信
        send_sms.delay(settings.RONGLIANYUN.get('reg_tid'), phone, datas=(captcha, time // 60))

        # 将验证码记录到redis中，并以time作为有效期
        pipe = redis.pipeline()
        pipe.multi()
        pipe.setex(f'sms_{phone}', time, captcha)
        pipe.setex(f'interval_{phone}', sms_interval, '_')
        pipe.execute()  # 提交事务，把pipeline的数据提交给redis

        return Response({'msg': 'OK'}, status=status.HTTP_200_OK)


class CourseListAPIView(ListAPIView):
    # 当前用户的课程列表信息
    permission_classes = [IsAuthenticated]
    serializer_class = UserCourseModelSerializer
    pagination_class = CourseListPagination

    def get_queryset(self):
        user = self.request.user
        query = UserCourse.objects.filter(user=user)
        course_type = int(self.request.query_params.get("type", -1))
        course_type_list = [item[0] for item in Course.COURSE_TYPE]
        if course_type in course_type_list:
            query = query.filter(course__course_type=course_type)
        return query.order_by("-id").all()

class UserCourseAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCourseModelSerializer

    def get(self,request,course_id):
        # 获取用户在当前课程的学习进度
        user = request.user
        try:
            user_course = UserCourse.objects.get(user=user, course=course_id)
        except UserCourse.DoesNotExist:
            return Response({"error": "当前课程您尚未购买！"}, status=status.HTTP_400_BAD_REQUEST)

        chapter_id = user_course.chapter_id
        print(f"chapter_id={chapter_id}")
        if chapter_id:
            # 曾经学习过本课程
            lesson = user_course.lesson
        else:
            # 从未学习当前课程
            # 获取当前课程第1个章节
            chapter = user_course.course.chapter_list.order_by("order").first()
            if not chapter:
                return Response({'error': '当前课程没有任何章节'}, status=status.HTTP_400_BAD_REQUEST)

            # 获取当前章节第1个课时
            lesson = chapter.lesson_list.order_by("order").first()
            if not lesson:
                return Response({'error': '当前章节没有任何课时'}, status=status.HTTP_400_BAD_REQUEST)

            # 保存本次学习起始进度
            user_course.chapter = chapter
            user_course.lesson = lesson
            user_course.save()

        serializer = self.get_serializer(user_course)
        data = serializer.data
        # 获取当前课时的课时类型和课时链接
        data["lesson_type"] = lesson.lesson_type
        data["lesson_link"] = lesson.lesson_link

        return Response(data)


class StudyLessonAPIView(APIView):
    # 用户在当前课时的学习时间进度
    permission_classes = [IsAuthenticated]

    def get(self, request):
        lesson_id = int(request.query_params.get("lesson"))
        user = request.user

        # 查找课时
        lesson = CourseLesson.objects.get(pk=lesson_id)

        progress = StudyProgress.objects.filter(user=user, lesson=lesson).first()

        # 如果查询没有进度，则默认进度为0
        if progress is None:
            progress = StudyProgress.objects.create(
                user=request.user,
                lesson=lesson,
                study_time=0
            )

        return Response(progress.study_time)


class StudyProgressAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 添加课时学习进度
        try:
            # 1. 接收客户端提交的视频进度和课时ID
            study_time = int(request.data.get("time"))
            lesson_id = int(request.data.get("lesson"))
            user = request.user

            # 判断当前课时是否免费或者当前课时所属的课程是否被用户购买了

            # 判断本次更新学习时间是否超出阈值，当超过阈值，则表示用户已经违规快进了。
            if study_time > constants.MAV_SEEK_TIME:
                raise Exception

            # 查找课时
            lesson = CourseLesson.objects.get(pk=lesson_id)

        except:
            return Response({"error": "无效的参数或当前课程信息不存在！"})

        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
                # 2. 记录课时学习进度
                progress = StudyProgress.objects.filter(user=user, lesson=lesson).first()

                if progress is None:
                    # 新增一条用户与课时的学习记录
                    progress = StudyProgress(
                        user=user,
                        lesson=lesson,
                        study_time=study_time
                    )
                else:
                    # 直接更新现有的学习时间
                    progress.study_time = int(progress.study_time) + int(study_time)

                progress.save()

                # 3. 记录课程学习的总进度
                user_course = UserCourse.objects.get(user=user, course=lesson.course)
                user_course.study_time = int(user_course.study_time) + int(study_time)

                # 用户如果往后观看章节，则记录下
                if lesson.chapter.orders > user_course.chapter.orders:
                    user_course.chapter = lesson.chapter

                # 用户如果往后观看课时，则记录下
                if lesson.orders > user_course.lesson.orders:
                    user_course.lesson = lesson

                user_course.save()

                return Response({"message": "课时学习进度更新完成！"})

            except Exception as e:
                print(f"error={e}")
                logger.error(f"更新课时进度失败！:{e}")
                transaction.savepoint_rollback(save_id)
                return Response({"error": "当前课时学习进度丢失！"})