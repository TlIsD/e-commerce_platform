from datetime import datetime
from rest_framework import serializers
from django_redis import get_redis_connection

import constants
from .models import Order, OrderDetail, Course
from coupon.models import  CouponLog
from django.db import transaction
import logging

logger = logging.getLogger('django')

class OrderModelSerializer(serializers.ModelSerializer):
    user_coupon_id = serializers.IntegerField(write_only=True, default=-1)
    order_timeout = serializers.IntegerField(read_only=True)

    class Meta:
        model = Order
        fields = ["pay_type", "id", "order_number", "user_coupon_id", "credit", "order_timeout"]
        read_only_fields = ["id", "order_number"]
        extra_kwargs = {
            "pay_type": {"write_only": True},
            "credit": {"write_only": True},
        }

    def create(self, validated_data):
        redis = get_redis_connection("cart")
        user = self.context["request"].user

        # 判断用户如果使用了优惠券，则优惠券需要判断验证
        user_coupon_id = validated_data.get("user_coupon_id")
        # 本次下单时，用户使用的优惠券
        user_coupon = None
        if user_coupon_id != -1:
            user_coupon = CouponLog.objects.filter(pk=user_coupon_id, user_id=user.id).first()

        # 本次下单时，用户使用的积分数量
        use_credit = validated_data.get("credit", 0)
        if use_credit > 0 and use_credit > user.credit:
            raise serializers.ValidationError(detail="拥有的积分不足以抵扣本次下单的积分，请重新下单！")

        with transaction.atomic():
            # 设置回滚点
            t1 = transaction.savepoint()

            try:
                # 创建订单记录
                order = Order.objects.create(
                    name="购买课程",  # 订单标题
                    user_id=user.id,  # 当前下单的用户ID

                    # 基于redis生成分布式唯一订单号
                    order_number=datetime.now().strftime("%Y%m%d") + ("%08d" % user.id) + "%08d" % redis.incr("order_number"),
                    pay_type=validated_data.get("pay_type"),  # 支付方式
                )

                # 记录本次下单的商品列表
                cart_hash = redis.hgetall(f"cart_{user.id}")
                if len(cart_hash) < 1:
                    raise serializers.ValidationError(detail="购物车没有要下单的商品")

                # 提取购物车中所有勾选状态为b'1'的商品
                course_id_list = [int(key.decode()) for key, value in cart_hash.items() if value == b'1']

                if len(course_id_list) < 1:
                    raise serializers.ValidationError(detail="购物车没有选择下单的商品")

                # 添加订单与课程的关系
                course_list = Course.objects.filter(pk__in=course_id_list, is_deleted=False, is_show=True).all()
                detail_list = []
                total_price = 0  # 本次订单的总价格
                real_price = 0  # 本次订单的实付总价

                # 用户使用优惠券或积分以后，在后端计算本次使用优惠券或积分的最大优惠额度
                total_discount_price = 0  # 总优惠价格
                max_discount_course = None  # 享受最大优惠的课程

                max_use_credit = 0  # 本次下单最多可用的抵扣积分

                for course in course_list:
                    discount_price = course.discount.get("price", None)  # 获取课程原价
                    if discount_price is not None:
                        discount_price = float(discount_price)

                    discount_name = course.discount.get("type", "")
                    detail_list.append(OrderDetail(
                        orders = order,
                        course = course,
                        name = course.name,
                        price = course.price,
                        real_price = course.price if discount_price is None else discount_price,
                        discount_name = discount_name,
                    ))

                    # 统计订单的总价和实付总价
                    total_price += float(course.price)
                    real_price += float(course.price if discount_price is None else discount_price)

                    # 在用户使用了优惠券，并且当前课程没有参与其他优惠活动时，找到最佳优惠课程
                    if user_coupon and discount_price is None:
                        if max_discount_course is None:
                            max_discount_course = course
                        else:
                            if course.price >= max_discount_course.price:
                                max_discount_course = course

                    # 添加每个课程的可用积分
                    if use_credit > 0 and course.credit > 0:
                        max_use_credit += course.credit

                # 在用户使用了优惠券以后，根据循环中得到的最佳优惠课程进行计算最终抵扣金额
                if user_coupon:
                    # 优惠公式
                    sale = float(user_coupon.coupon.sale[1:])
                    if user_coupon.coupon.discount == 1:
                        # 减免优惠券
                        total_discount_price = sale
                    elif user_coupon.coupon.discount == 2:
                        # 折扣优惠券
                        total_discount_price = float(max_discount_course.price) * (1 - sale)
                # 一次性批量添加本次下单的商品记录
                OrderDetail.objects.bulk_create(detail_list)

                if use_credit > 0:
                    if max_use_credit < use_credit:
                        raise serializers.ValidationError(detail="本次使用的抵扣积分数额超过了限制！")

                    # 当前订单添加积分抵扣的数量
                    order.credit = use_credit
                    total_discount_price = float(use_credit / constants.CREDIT_TO_MONEY)

                    # todo 扣除用户拥有的积分，订单超时未支付，返还订单中对应数量的积分给用户。如果订单成功支付，则添加一个积分流水记录。
                    user.credit = user.credit - use_credit
                    user.save()

                # 保存订单的总价格和实付价格
                order.total_price = real_price
                order.real_price = float(real_price - total_discount_price)
                order.save()

                # 删除购物车中被勾选的商品
                cart = {key: value for key, value in cart_hash.items() if value == b'0'}
                pipe = redis.pipeline()
                pipe.multi()
                # 删除原来的购物车
                pipe.delete(f"cart_{user.id}")
                # 重新把未勾选的商品记录到购物车中
                if cart:
                    pipe.hmset(f"cart_{user.id}", cart)
                pipe.execute()

                # 如果有使用了优惠券，则把优惠券和当前订单进行绑定
                if user_coupon:
                    user_coupon.order = order
                    user_coupon.save()
                    # 把优惠券从redis中移除
                    redis = get_redis_connection("coupon")
                    redis.delete(f"{user.id}:{user_coupon_id}")

                order.order_timeout = constants.ORDER_TIMEOUT

                return order

            except Exception as e:
                # 事务回滚
                transaction.savepoint_rollback(t1)
                # 日志记录
                logger.error(f'订单创建失败：{e}')

                raise serializers.ValidationError(detail='订单创建失败')


class OrderDetailSerializer(serializers.ModelSerializer):
    # 订单详情序列化器
    # 通过source修改数据源，可以把需要调用的部分外键字段提取到当前序列化器中
    course_id = serializers.IntegerField(source="course.id")
    course_name = serializers.CharField(source="course.name")
    course_cover = serializers.ImageField(source="course.course_cover")

    class Meta:
        model = OrderDetail
        fields = ["id", "price", "real_price", "discount_name", "course_id", "course_name", "course_cover"]


class OrderListModelSerializer(serializers.ModelSerializer):
    # 订单列表序列化器
    order_courses = OrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "order_number", "total_price", "real_price", "pay_time", "created_time", "credit", "coupon", "pay_type", "order_status", "order_courses"]
