import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.captcha.v20190722 import captcha_client, models
from django.conf import settings

class TencentCloudApi(object):
    # 腾讯云API操作工具类
    def __init__(self):
        self.cred = credential.Credential(settings.TENCENTCLOUD['SecretId'], settings.TENCENTCLOUD["SecretKey"])

    def captcha(self, ticket, randstr, user_ip):
        try:
            Captcha = settings.TENCENTCLOUD["Captcha"]

            params = {
                # 验证码类型int固定为9
                "CaptchaType": Captcha["CaptchaType"],
                # 客户端提交的临时票据
                "Ticket": ticket,
                # 客户端ip地址
                "UserIp": user_ip,
                # 随机字符串
                "Randstr": randstr,
                # 验证码应用ID类型为int
                "CaptchaAppId": Captcha["CaptchaAppId"],
                # 验证码应用key
                "AppSecretKey": Captcha["AppSecretKey"],
            }

            # 实例化http请求工具类
            httpProfile = HttpProfile()
            # 设置API所在服务器域名
            httpProfile.endpoint = Captcha["endpoint"]
            # 实例化客户端工具类
            clientProfile = ClientProfile()
            # 给客户端绑定请求的服务端域名
            clientProfile.httpProfile = httpProfile
            # 实例化验证码服务端请求工具的客户端对象
            client = captcha_client.CaptchaClient(self.cred, "", clientProfile)
            # 客户端请求对象参数的初始化
            req = models.DescribeCaptchaResultRequest()

            # 发送请求
            req.from_json_string(json.dumps(params))
            # 获取腾讯云的响应结果
            resp = client.DescribeCaptchaResult(req)
            # 把响应结果转换成json格式数据
            result = json.loads(resp.to_json_string())

            return result and result.get("CaptchaCode") == 1

        except Exception as err:
            print(f'err：{err}')
            raise TencentCloudSDKException