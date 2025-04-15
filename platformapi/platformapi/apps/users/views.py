from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken

from .models import User
from platformapi.utils.tencentcloudapi import TencentCloudApi, TencentCloudSDKException
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class LoginAPIView(ObtainJSONWebToken):
    # 登录视图
    def post(self, request, *args, **kwargs):
        try:
            api = TencentCloudApi()

            result = api.captcha(
                request.data.get("ticket"),
                request.data.get("randstr"),
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
    def get(self, request, phone):
        try:
            User.objects.get(phone=phone)
            return Response({'err': '当前手机号已被注册'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'msg': 'OK'}, status=status.HTTP_200_OK)