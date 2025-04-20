import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'platformapi.settings.dev')

# 实例化celery应用对象
app = Celery('platform')

# 指定任务的队列名称
app.conf.tasks_from_queue = 'Celery'

# 也可以把配置写在django的项目配置中
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动根据配置查找django的所有子应用下的tasks任务文件
app.autodiscover_tasks()