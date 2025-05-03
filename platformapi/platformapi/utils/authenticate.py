from django.contrib.auth.management.commands.changepassword import UserModel
from django.db.models import Q
from django_redis import get_redis_connection
from rest_framework_jwt.utils import jwt_payload_handler as payload_handler
from django.contrib.auth.backends import ModelBackend, UserModel
from rest_framework_jwt.settings import api_settings

def jwt_payload_handler(user):
    # 自定义载荷信息
    # 先生成原有的载荷信息
    payload = payload_handler(user)

    # 增加
    if hasattr(user, 'avatar'):
        payload['avatar'] = user.avatar.url if user.avatar else ""
    if hasattr(user, 'nickname'):
        payload['nickname'] = user.nickname

    if hasattr(user, 'money'):
        payload['money'] = float(user.money)
    if hasattr(user, 'credit'):
        payload['credit'] = user.credit

    return payload

def jwt_response_payload_handler(token, user, request):
    # 增加返回购物车的商品数量
    redis = get_redis_connection("cart")
    cart_total = redis.hlen(f"cart_{user.id}")

    return {
        "cart_total": cart_total,
        "token": token
    }

def get_user_by_account(account):
    # 根据用户名或手机号或邮箱获取user
    user = UserModel.objects.filter(Q(username=account) | Q(phone=account) | Q(email=account)).first()
    return user

class CustomAuthBackend(ModelBackend):
    # 自定义用户认证类
    def authenticate(self, request, username=None, password=None, *args, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        if username is None or password is None:
            return

        # 根据用户名信息获取账户信息
        user = get_user_by_account(username)
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user

def generate_jwt_token(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    # 生成载荷
    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)