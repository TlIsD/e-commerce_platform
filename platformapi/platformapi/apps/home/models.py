from django.utils.safestring import mark_safe

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


class Banner(BaseModel):
    image = models.ImageField(upload_to='banner/%y/', verbose_name='banner图片地址')
    link = models.CharField(max_length=255, verbose_name='链接')
    note = models.CharField(max_length=255, verbose_name='备注')
    is_http = models.BooleanField(default=False, verbose_name='是否为外链', help_text="站外链接地址")

    class Meta:
        db_table = 'ec_banner'
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def image_html(self):
        if self.image:
            return mark_safe(f'<img src="{ self.image.url }" style="border-radius: 0%; max-height: 100px; max-width: 400px" />')
        return ''

    image_html.short_description = '广告图片'
    image_html.allow_tags = True
    image_html.admin_order_field = 'image'