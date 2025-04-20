import os, django
from celery import Celery

# 初始化django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'platformapi.settings.dev')
django.setup()

app = Celery('platform')

# 加载配置文件
app.config_from_object('mycelery.settings')

# 注册任务
app.autodiscover_tasks(['mycelery.sms'])

# 在项目根目录启动
# celery -A mycelery.main worker --loglevel=info