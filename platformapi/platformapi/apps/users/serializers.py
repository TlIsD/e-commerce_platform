from rest_framework import serializers
from .models import User
from rest_framework_jwt.settings import api_settings
import re, constants
from platformapi.utils.tencentcloudapi import TencentCloudApi, TencentCloudSDKException


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

            # todo 验证短信验证码

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
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        # 生成载荷
        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)

        return user
