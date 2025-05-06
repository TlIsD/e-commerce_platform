import json
from django.utils.timezone import datetime
from django.contrib import admin
from django_redis import get_redis_connection
from .models import Coupon, CouponDirection, CouponCourseCat, CouponCourse, CouponLog


# Register your models here.
class CouponDirectionInLine(admin.TabularInline):
    # 学习方向的内嵌类
    model = CouponDirection
    fields = ["id", "direction"]


class CouponCourseCatInLine(admin.TabularInline):
    # 课程分类的内嵌类
    model = CouponCourseCat
    fields = ["id", "category"]


class CouponCourseInLine(admin.TabularInline):
    # 课程信息的内嵌类
    model = CouponCourse
    fields = ["id", "course"]


class CouponModelAdmin(admin.ModelAdmin):
    # 优惠券的模型管理器
    list_display = ["id", "name", "start_time", "end_time", "total", "has_total", "coupon_type", "get_type", ]
    inlines = [CouponDirectionInLine, CouponCourseCatInLine, CouponCourseInLine]


admin.site.register(Coupon, CouponModelAdmin)


class CouponLogModelAdmin(admin.ModelAdmin):
    # 优惠券发放和使用日志
    list_display = ["id", "user", "coupon", "orders", "use_time", "use_status"]

    def save_model(self, request, obj, form, change):
        # 保存或更新记录时自动执行的钩子
        obj.save()
        # 同步记录到redis中
        redis = get_redis_connection("coupon")

        if obj.use_status == 0 and obj.use_time is None:
            # 记录优惠券信息到redis中
            pipe = redis.pipeline()
            pipe.multi()
            pipe.hset(f"{obj.user.id}:{obj.id}", "coupon_id", obj.coupon.id)
            pipe.hset(f"{obj.user.id}:{obj.id}", "name", obj.coupon.name)
            pipe.hset(f"{obj.user.id}:{obj.id}", "discount", obj.coupon.discount)
            pipe.hset(f"{obj.user.id}:{obj.id}", "get_discount_display", obj.coupon.get_discount_display())
            pipe.hset(f"{obj.user.id}:{obj.id}", "coupon_type", obj.coupon.coupon_type)
            pipe.hset(f"{obj.user.id}:{obj.id}", "get_coupon_type_display", obj.coupon.get_coupon_type_display())
            pipe.hset(f"{obj.user.id}:{obj.id}", "start_time", obj.coupon.start_time.strftime("%Y-%m-%d %H:%M:%S"))
            pipe.hset(f"{obj.user.id}:{obj.id}", "end_time", obj.coupon.end_time.strftime("%Y-%m-%d %H:%M:%S"))
            pipe.hset(f"{obj.user.id}:{obj.id}", "get_type", obj.coupon.get_type)
            pipe.hset(f"{obj.user.id}:{obj.id}", "get_get_type_display", obj.coupon.get_get_type_display())
            pipe.hset(f"{obj.user.id}:{obj.id}", "condition", obj.coupon.condition)
            pipe.hset(f"{obj.user.id}:{obj.id}", "sale", obj.coupon.sale)
            pipe.hset(f"{obj.user.id}:{obj.id}", "to_direction", json.dumps(list(obj.coupon.to_direction.values("direction__id", "direction__name"))))
            pipe.hset(f"{obj.user.id}:{obj.id}", "to_category", json.dumps(list(obj.coupon.to_category.values("category__id", "category__name"))))
            pipe.hset(f"{obj.user.id}:{obj.id}", "to_course", json.dumps(list(obj.coupon.to_course.values("course__id", "course__name"))))
            # 设置当前优惠券的有效期
            pipe.expire(f"{obj.user.id}:{obj.id}", int(obj.coupon.end_time.timestamp() - datetime.now().timestamp()))
            pipe.execute()
        else:
            redis.delete(f"{obj.user.id}:{obj.id}")

    def delete_model(self, request, obj):
        # 删除记录时自动执行的钩子
        # 如果系统后台管理员删除当前优惠券记录，则redis中的对应记录也被删除
        print(obj, "详情页中删除一个记录")
        redis = get_redis_connection("coupon")
        redis.delete(f"{obj.user.id}:{obj.id}")
        obj.delete()

    def delete_queryset(self, request, queryset):
        # 删除优惠券记录时，同时删除redis中的记录
        print(queryset, "列表页中删除多个记录")
        redis = get_redis_connection("coupon")
        for obj in queryset:
            redis.delete(f"{obj.user.id}:{obj.id}")
        queryset.delete()

admin.site.register(CouponLog, CouponLogModelAdmin)