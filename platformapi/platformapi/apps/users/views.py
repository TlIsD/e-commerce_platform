from rest_framework.generics import CreateAPIView
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
