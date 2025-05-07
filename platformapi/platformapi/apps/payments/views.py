from datetime import datetime

from django.conf import settings
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from courses.serializers import CourseInfoSerializer
from orders.models import Order
from alipay import AliPay
from alipay.utils import AliPayConfig
from alipaysdk import AliPaySDK

# Create your views here.
class AlipayAPIViewSet(ViewSet):
    # 支付宝接口

    def link(self, request, order_number):
        # 生成支付宝支付链接信息
        try:
            order = Order.objects.get(order_number=order_number)
            if order.order_status > 0:
                return Response({"message": "对不起，当前订单不能重复支付或订单已超时！"})
        except Order.DoesNotExist:
            return Response({"message": "对不起，当前订单不存在！"})

        alipay = AliPaySDK()
        link = alipay.page_pay(order_number, order.real_price, order.name)
        print(link)

        return Response({
            "pay_type": 0, # 支付类型
            "get_pay_type_display": "支付宝", # 支付类型的提示
            "link": link  # 支付连接地址
        })

    def return_result(self, request):
        # 支付宝支付结果的同步通知处理
        data = request.query_params.dict()
        alipay = AliPaySDK()
        success = alipay.check_sign(data)
        if not success:
            return Response({"errmsg": "通知结果不存在！"}, status=status.HTTP_400_BAD_REQUEST)

        order_number = data.get("out_trade_no")
        try:
            order = Order.objects.get(order_number=order_number)
            if order.order_status > 1:
                return Response({"errmsg": "订单超时或已取消！"}, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"errmsg": "订单不存在！"}, status=status.HTTP_400_BAD_REQUEST)

        # 获取当前订单相关的课程信息，用于返回给前端
        order_courses = order.order_courses.all()
        course_list = [item.course for item in order_courses]

        if order.order_status == 0:
            result = alipay.query(order_number)

            if result.get("trade_status", None) in ["TRADE_FINISHED", "TRADE_SUCCESS"]:
                # 支付成功
                # todo 1. 修改订单状态
                order.pay_time = datetime.now()
                order.order_status = 1
                order.save()
                # todo 2. 记录扣除个人积分的流水信息，补充个人的优惠券使用记录
                # todo 3. 用户和课程的关系绑定
                # todo 4. 取消订单超时

        # 返回客户端结果
        serializer = CourseInfoSerializer(course_list, many=True)
        return Response({
            "pay_time": order.pay_time.strftime("%Y-%m-%d %H:%M:%S"),
            "real_price": float(order.real_price),
            "course_list": serializer.data
        })