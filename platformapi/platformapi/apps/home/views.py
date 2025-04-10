from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_redis import get_redis_connection

import logging
# 调用日志
logger = logging.getLogger('django')

# Create your views here.
class HomeAPIView(APIView):
    def get(self, request):
        # 测试日志功能
        # logger.error('ERROR')
        # logger.info('INFO')

        # 测试redis功能
        redis = get_redis_connection('sms_code')
        brother = redis.lrange('brother', 0, -1)

        return Response(brother, status.HTTP_200_OK)