import random
from django.conf import settings
# from ronglianyunapi import send_sms
# from mycelery.sms.tasks import send_sms
from .tasks import send_sms
from django_redis import get_redis_connection
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken

from .models import User
from platformapi.utils.tencentcloudapi import TencentCloudApi, TencentCloudSDKException
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserRegisterSerializer

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