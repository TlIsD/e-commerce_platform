from django.db import models


class BaseModel(models.Model):
    # 公共模型
    order = models.IntegerField(default=0, verbose_name='序号')
    name = models.CharField(max_length=255, default='', verbose_name='标题')
    is_show = models.BooleanField(default=True, verbose_name='是否显示')
    is_deleted = models.BooleanField(default=False, verbose_name='是否被删除')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        abstract = True