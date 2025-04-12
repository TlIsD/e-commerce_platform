from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    mobile = models.CharField(max_length=15, unique=True, verbose_name='手机号')
    money = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='账户余额')
    credit = models.IntegerField(default=0, verbose_name='积分')
    avatar = models.ImageField(upload_to='avatar/%y', null=True, default='/default.jpg', verbose_name='头像')
    nickname = models.CharField(max_length=50, default='', null=True, verbose_name='昵称')

    class Meta:
        db_table = 'ec_users'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
