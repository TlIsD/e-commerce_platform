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

    def get(self, request):
        # 获取购物车中商品列表
        user_id = request.user.id
        redis = get_redis_connection("cart")
        cart_hash = redis.hgetall(f"cart_{user_id}")
        """
        cart_hash = {
            b'商品课程ID': b'勾选状态', 
            b'2': b'1', 
            b'4': b'1', 
        }
        """
        if len(cart_hash) < 1:
            return Response({"error": "购物车没有任何商品。"})

        cart = [(int(key.decode()), bool(value.decode())) for key, value in cart_hash.items()]
        # cart = [ (2,True)， (4,True) ]
        course_id_list = [item[0] for item in cart]
        course_list = Course.objects.filter(pk__in=course_id_list, is_deleted=False, is_show=True).all()
        data = []
        for course in course_list:
            data.append({
                "id": course.id,
                "name": course.name,
                "course_cover": course.course_cover.url,
                "price": float(course.price),
                "discount": course.discount,
                "course_type": course.get_course_type_display(),
                # 勾选状态：把课程ID转换成bytes类型，判断当前ID是否在购物车字典中作为key存在，如果存在，判断当前课程ID对应的值是否是字符串"1"，是则返回True
                "selected": (str(course.id).encode() in cart_hash) and cart_hash[str(course.id).encode()].decode() == "1"
            })
        return Response({"msg": "ok！", "cart": data})

    def patch(self, request):
        # 切换购物车中商品勾选状态
        # 获取该购物车的用户
        user_id = request.user.id
        # 获取购物车的课程ID与勾选状态
        course_id = int(request.data.get("course_id", 0))
        selected = int(bool(request.data.get("selected", True)))

        redis = get_redis_connection("cart")

        try:
            Course.objects.get(pk=course_id, is_show=True, is_deleted=False)
        except Course.DoesNotExist:
            redis.hdel(f"cart_{user_id}", course_id)
            return Response({"errmsg": "当前商品不存在或已经被下架！！"})

        redis.hset(f"cart_{user_id}", course_id, selected)
        return Response({"msg": "ok"})

    def put(self, request):
        # 全选/全不选
        user_id = request.user.id
        selected = int(bool(request.data.get("selected", True)))
        redis = get_redis_connection("cart")

        # 获取购物车中所有商品课程信息
        cart_hash = redis.hgetall(f"cart_{user_id}")
        if len(cart_hash) < 1:
            return Response({"errmsg": "购物车没有任何商品。"}, status=status.HTTP_204_NO_CONTENT)

        # 把redis中的购物车课程ID信息转换成普通列表
        cart_list = [int(course_id.decode()) for course_id in cart_hash]

        # 批量修改购物车中素有商品课程的勾选状态
        pipe = redis.pipeline()
        pipe.multi()
        for course_id in cart_list:
            pipe.hset(f"cart_{user_id}", course_id, selected)
        pipe.execute()

        return Response({"msg": "ok"})
