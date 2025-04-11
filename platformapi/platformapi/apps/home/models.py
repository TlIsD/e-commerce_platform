from models import BaseModel, models

# Create your models here.
class Nav(BaseModel):
    # 导航菜单
    position_choices = (
        (0, "Header"),
        (1, "Footer"),
    )

    is_http = models.BooleanField(default=False , verbose_name='是否为外链')
    position = models.IntegerField(choices=position_choices, default=0, verbose_name='导航位置')
    link = models.CharField(max_length=255, verbose_name='链接')

    class Meta:
        db_table = 'ec_nav'
        verbose_name = '导航菜单'
        verbose_name_plural = verbose_name