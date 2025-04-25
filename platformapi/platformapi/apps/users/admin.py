from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, _
from .models import User
# Register your models here.

class UserModelAdmin(UserAdmin):
    # 用户信息
    list_display = ["id", "username", "avatar_small", "money", "credit", "phone"]
    fieldsets = (
        (None, {'fields': ('username', 'password', 'avatar')}),
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


admin.site.register(User, UserModelAdmin)
