from django.conf import settings
from alipay import AliPay
from alipay.utils import AliPayConfig
from datetime import datetime

class AliPaySDK(AliPay):
    # 支付宝接口sdk工具类
    def __init__(self, config=None):
        if config is None:
            self.config = settings.ALIPAY
        else:
            self.config = config

        app_private_key_string = open(self.config["app_private_key_path"]).read()
        alipay_public_key_string = open(self.config["alipay_public_key_path"]).read()
        super().__init__(
            appid=self.config["appid"],
            app_notify_url=self.config["notify_url"],  # 默认全局回调 url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type=self.config["sign_type"],  # RSA 或者 RSA2
            debug=self.config["debug"],  # 默认 False，沙箱模式下必须设置为True
            verbose=self.config["verbose"],  # 输出调试数据
            config=AliPayConfig(timeout=self.config["timeout"])  # 可选，请求超时时间，单位：秒
        )

    def page_pay(self,order_number,real_price,order_name):
        # 生成支付链接
        order_string = self.client_api(
            "alipay.trade.page.pay",
            biz_content={
                "out_trade_no": order_number,  # 订单号
                "total_amount": float(real_price),  # 订单金额
                "subject": order_name,  # 订单标题
                "product_code": "FAST_INSTANT_TRADE_PAY",
            },
            return_url=self.config["return_url"],  # 可选，同步回调地址，必须填写客户端的路径
            notify_url=self.config["notify_url"]  # 可选，不填则使用采用全局默认notify_url，必须填写服务端的路径
        )

        return f"{self.config['gateway']}?{order_string}"

    def check_sign(self, data):
        # 验证返回的支付结果中的签证信息
        signature = data.pop("sign")
        success = self.verify(data, signature)
        return success

    def query(self,order_number):
        # 根据订单号查询订单状态
        return self.server_api(
            "alipay.trade.query",
            biz_content={
                "out_trade_no": order_number
            }
        )

    def refund(self,order_number, real_price):
        # 退款
        self.server_api(
            "alipay.rade.refund",
            biz_content={
                "out_trade_no": order_number,
                "refund_amount": real_price
            }
        )

    def transfer(self, account,amount):
        # 转账给个人
        return self.server_api(
            "alipay.fund.trans.toaccount.transfer",
            biz_content = {
                "out_biz_no": datetime.now().strftime("%Y%m%d%H%M%S"),
                "payee_type": "ALIPAY_LOGONID/ALIPAY_USERID",
                "payee_account": account,
                "amount": amount
            }
        )