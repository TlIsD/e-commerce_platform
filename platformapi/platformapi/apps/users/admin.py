from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, _
from .models import User, Credit


# Register your models here.

class UserModelAdmin(UserAdmin):
    # 用户信息
    list_display = ["id", "username", "avatar_small", "money", "credit", "phone"]
    list_editable = ["credit"]

    fieldsets = (
        (None, {'fields': ('username', 'password', 'credit', 'avatar')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    ordering = ('id',)

    def save_model(self, request, obj, form, change):
        if change:
            # 更新数据
            user = User.objects.get(pk=obj.id)
            has_credit = user.credit  # 原来用户的积分数据
            new_credit = obj.credit  # 更新后用户的积分数据

            Credit.objects.create(
                user=user,
                number=int(new_credit - has_credit),
                operation=2,
            )

        obj.save()

        if not change:
            # 新增数据
            Credit.objects.create(
                user=obj.id,
                number=obj.credit,
                operation=2,
            )

admin.site.register(User, UserModelAdmin)


class CreditModelAdmin(admin.ModelAdmin):
    # 积分流水的模型管理器
    list_display = ["id","user","number","__str__"]

admin.site.register(Credit,CreditModelAdmin)