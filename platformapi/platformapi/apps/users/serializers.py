from django_redis import get_redis_connection
from rest_framework import serializers
from .models import User, UserCourse
from rest_framework_jwt.settings import api_settings
import re, constants
from platformapi.utils.tencentcloudapi import TencentCloudApi, TencentCloudSDKException
from authenticate import generate_jwt_token


class UserRegisterSerializer(serializers.ModelSerializer):
    # 注册序列化器
    sms_captcha = serializers.CharField(min_length=4, max_length=6, required=True, write_only=True, help_text='验证码')
    ticket = serializers.CharField(write_only=True, required=True, help_text='临时凭证')
    randstr = serializers.CharField(write_only=True, required=True, help_text='随机字符串')
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['phone', 'password', 'sms_captcha', 'token', 'ticket', 'randstr']
        extra_kwargs = {
            'phone': {
                'required': True,
                'write_only': True,
            },
            'password': {
                'required': True,
                'write_only': True,
                'min_length': 6,
                'max_length': 16,
            }
        }

    def validate(self, data):
        print(data)
        # 验证客户端数据
        phone = data.get('phone', None)
        if not re.match(r'^1[3-9]\d{9}$', phone):
            raise serializers.ValidationError(detail='手机号格式不正确！', code='phone')

        try:
            User.objects.get(phone=phone)
            # 防止快速点击造成的反复注册
            raise serializers.ValidationError(detail='该手机号已注册')
        except User.DoesNotExist:
            pass

        # 验证防水墙验证码
        api = TencentCloudApi()

        result = api.captcha(
            data.get("ticket"),
            data.get("randstr"),
            self.context['request']._request.META.get("REMOTE_ADDR"),
        )
        if not result:
            raise serializers.ValidationError(detail='验证码校验失败！')

        # 验证短信验证码
        redis = get_redis_connection('sms_code')
        code = redis.get(f"sms_{phone}")
        if code is None:
            raise serializers.ValidationError(detail='验证码已失效', code='sms_captcha')

        if code.decode() != data.get('sms_captcha'):
            raise serializers.ValidationError(detail='验证码错误', code='sms_captcha')

        redis.delete(f"sms_{phone}")

        return data

    def create(self, validated_data):
        validated_data.pop('sms_captcha', None)
        validated_data.pop('ticket', None)
        validated_data.pop('randstr', None)

        # 保存用户信息
        phone = validated_data.get('phone')
        password = validated_data.get('password')

        user = User.objects.create_user(
            username=phone,
            password=password,
            phone=phone,
            avatar=constants.DEFAULT_AVATAR
        )

        # 注册后免登录
        user.token = generate_jwt_token(user)

        return user

class UserCourseModelSerializer(serializers.ModelSerializer):
    # 用户课程信息序列化器
    course_cover = serializers.ImageField(source="course.course_cover")
    course_name = serializers.CharField(source="course.name")
    chapter_name = serializers.CharField(source="chapter.name", default="")
    chapter_id = serializers.IntegerField(source="chapter.id", default=0)
    chapter_orders = serializers.IntegerField(source="chapter.orders", default=0)
    lesson_id = serializers.IntegerField(source="lesson.id", default=0)
    lesson_name = serializers.CharField(source="lesson.name", default="")
    lesson_orders = serializers.IntegerField(source="lesson.orders", default=0)
    course_type = serializers.IntegerField(source="course.course_type", default=0)
    get_course_type_display = serializers.CharField(source="course.get_course_type_display",default="")

    class Meta:
        model = UserCourse
        fields = ["course_id", "course_cover",  "course_name", "study_time", "chapter_id", "chapter_orders", "chapter_name",
                  "lesson_id", "lesson_orders", "lesson_name","course_type", "get_course_type_display", "progress",
                  "note", "qa", "code"]