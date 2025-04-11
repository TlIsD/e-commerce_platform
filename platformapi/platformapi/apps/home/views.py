from rest_framework.generics import ListAPIView
from .models import Nav
from .serializers import NavSerializer

import constants

class NavHeaderListAPIView(ListAPIView):
    # 顶部导航
    queryset = Nav.objects.filter(position=constants.NAV_HEADER_POSITION, is_show=True, is_deleted=False).order_by('order', '-id')[:constants.NAV_HEADER_SIZE]
    serializer_class = NavSerializer



class NavFooterListAPIView(ListAPIView):
    # 脚部导航
    queryset = Nav.objects.filter(position=constants.NAV_FOOTER_POSITION,  is_show=True, is_deleted=False).order_by('order', '-id')[:constants.NAV_FOOTER_SIZE]
    serializer_class = NavSerializer