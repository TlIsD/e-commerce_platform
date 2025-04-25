from django.contrib import admin
from .models import Nav, Banner


# Register your models here.
class NavModelAdmin(admin.ModelAdmin):
    # 导航菜单的模型管理器
    list_display = ["id","name","link","is_http"]


admin.site.register(Nav, NavModelAdmin)


class BannerModelAdmin(admin.ModelAdmin):
    # 轮播广告的模型管理器
    list_display = ["id","image_html","link","is_http"]


admin.site.register(Banner, BannerModelAdmin)
