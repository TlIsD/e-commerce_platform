from ..main import app
from ronglianyunapi import send_sms as send_sms_to_user

@app.task(name = 'send_sms1')
def send_sms1():
    # 没有任何参数的异步任务
    print('sendsms任务1已执行')

@app.task(name = 'send_sms2')
def send_sms2(phone, code):
    # 有参数,没有结构的异步任务
    print(f'任务2执行了...phone={phone}, code={code}')

@app.task(name = 'send_sms3')
def send_sms3():
    # 没有参数,有结果的异步任务
    print('任务3执行了...')
    return 100

@app.task(name = 'send_sms4')
def send_sms4(x, y):
    # 都有的异步任务
    print('任务4执行了...')
    return x+y

@app.task(name = 'send_sms')
def send_sms(tid, phone, datas):
    # 发送短信
    return send_sms_to_user(tid, phone, datas)