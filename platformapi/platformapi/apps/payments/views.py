from django.conf import settings
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from orders.models import Order
from alipay import AliPay
from alipay.utils import AliPayConfig


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

        # 读取支付宝公钥与商户私钥
        app_private_key_string = open(settings.ALIPAY["app_private_key_path"]).read()
        alipay_public_key_string = open(settings.ALIPAY["alipay_public_key_path"]).read()

        # 创建alipay SDK操作对象
        alipay = AliPay(
            appid=settings.ALIPAY["appid"],
            app_notify_url=settings.ALIPAY["notify_url"],  # 默认全局回调 url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥
            alipay_public_key_string=alipay_public_key_string,
            sign_type=settings.ALIPAY["sign_type"],  # RSA2
            debug=settings.ALIPAY["debug"],  # 默认 False，沙箱模式下必须设置为True
            verbose=settings.ALIPAY["verbose"],  # 输出调试数据
            config=AliPayConfig(timeout=settings.ALIPAY["timeout"])  # 可选，请求超时时间，单位：秒
        )

        # 生成支付信息
        order_string = alipay.client_api(
            "alipay.trade.page.pay",  # 接口名称
            biz_content={
                "out_trade_no": order_number,  # 订单号
                "total_amount": float(order.real_price),  # 订单金额 单位：元
                "subject": order.name,  # 订单标题
                "product_code": "FAST_INSTANT_TRADE_PAY",  # 产品码，目前只能支持 FAST_INSTANT_TRADE_PAY
            },
            return_url=settings.ALIPAY["return_url"],  # 可选，同步回调地址，必须填写客户端的路径
            notify_url=settings.ALIPAY["notify_url"]   # 可选，不填则使用采用全局默认notify_url，必须填写服务端的路径
        )

        # 拼接完整的支付链接
        link = f"{settings.ALIPAY['gateway']}?{order_string}"
        print(link)

        return Response({
            "pay_type": 0, # 支付类型
            "get_pay_type_display": "支付宝", # 支付类型的提示
            "link": link  # 支付连接地址
        })