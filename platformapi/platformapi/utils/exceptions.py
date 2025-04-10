from rest_framework.views import exception_handler
from django.db import DatabaseError
from rest_framework.response import Response
from rest_framework import status
from redis import RedisError
import logging


logger = logging.getLogger('django')


# 自定义异常处理
def custom_exception_handler(exc, context):
    # exc: 异常类  context: 抛出异常的上下文
    # 调用drf框架原生的异常处理方法
    response = exception_handler(exc, context)  # 响应对象

    if response is None:
        view = context['view']
        if isinstance(exc, DatabaseError):
            # 数据库异常
            logger.error('MySQL异常！[%s] %s' % (view, exc))
            response = Response({'message': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

        elif isinstance(exc, RedisError):
            logger.error('Redis异常！[%s] %s' % (view, exc))
            response = Response({'message': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

        elif isinstance(exc, ZeroDivisionError):
            response = Response({'message': '0不能作为除数！'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response