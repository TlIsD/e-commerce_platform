from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import constants
from .services import get_user_coupon_list, get_user_enable_coupon_list

# Create your views here.

class CouponListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 获取用户拥有的所有优惠券
        user_id = request.user.id
        coupon_data = get_user_coupon_list(user_id)
        return Response(coupon_data)


class EnableCouponListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 获取用户拥有的本次下单可用所有优惠券及积分
        user_id = request.user.id
        coupon_data = get_user_enable_coupon_list(user_id)
        return Response({
            "msg": "ok",
            'has_credit': request.user.credit,
            'credit_to_money': constants.CREDIT_TO_MONEY,
            "coupon_list": coupon_data
        })