from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_redis import get_redis_connection
from courses.models import Course

# Create your views here.
class CartAPIView(APIView):
    # 用户必须登录才能调用当前视图
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # 添加课程商品到购物车中
        # 1. 接受客户端提交的商品信息：用户ID，课程ID，勾选状态
        user_id = request.user.id
        course_id = request.data.get("course_id", None)
        selected = 1  # 默认商品是勾选状态的
        print(f"user_id={user_id},course_id={course_id}")

        # 2. 验证课程是否允许购买[is_show=True, is_deleted=False]
        try:
            # 判断课程是否存在
            # todo 判断用户是否已经购买了
            course = Course.objects.get(is_show=True, is_deleted=False, pk=course_id)
        except:
            return Response({"errmsg": "该课程不存在！"}, status=status.HTTP_400_BAD_REQUEST)

        # 3. 添加商品到购物车
        redis = get_redis_connection("cart")
        '''
        cart_用户ID: {
           课程ID: 勾选状态
        }
        '''
        redis.hset(f"cart_{user_id}", course_id, selected)

        # 4. 获取购物车中的商品课程数量
        cart_total = redis.hlen(f"cart_{user_id}")

        # 5. 返回结果给客户端
        return Response({"msg": "成功添加商品课程到购物车！", "cart_total": cart_total}, status=status.HTTP_201_CREATED)