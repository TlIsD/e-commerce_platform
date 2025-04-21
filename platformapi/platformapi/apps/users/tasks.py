from celery import shared_task
from ronglianyunapi import send_sms as sms

import logging
logger = logging.getLogger('django')


@shared_task(name = 'send_sms')
def send_sms(tid, phone, datas):
    # 异步发送短信
    try:
        return sms(tid, phone, datas)
    except Exception as e:
        logger.error(f'手机号：{phone}, 短信发送失败：{e}')


@shared_task(name = 'send_sms1')
def send_sms1():
    print('send_sms1执行了......')
