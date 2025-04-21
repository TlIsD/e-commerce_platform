import json
from ronglian_sms_sdk import SmsSDK
from django.conf import settings


def send_sms(tid, phone, datas):
    # tid短信模版ID phone接收短信的手机号 datas短信模版的参数列表
    ronglianyun = settings.RONGLIANYUN
    sdk = SmsSDK(ronglianyun.get('accId'), ronglianyun.get('accToken'), ronglianyun.get('appId'))
    resp = sdk.sendMessage(tid, phone, datas)

    response = json.loads(resp)
    print(response, type(response))

    return response.get('statusCode') == '000000'
