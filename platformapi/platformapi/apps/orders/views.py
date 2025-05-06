from rest_framework.generics import CreateAPIView
from .models import Order
from .serializers import OrderModelSerializer
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class OrderCreateAPIView(CreateAPIView):
    # 创建订单
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer