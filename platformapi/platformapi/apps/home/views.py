from views import CachedListAPIView
from .models import Nav, Banner
from .serializers import NavSerializer, BannerSerializer

import constants

class NavHeaderListAPIView(CachedListAPIView):
    # 顶部导航
    queryset = Nav.objects.filter(position=constants.NAV_HEADER_POSITION, is_show=True, is_deleted=False).order_by('order', '-id')[:constants.NAV_HEADER_SIZE]
    serializer_class = NavSerializer


class NavFooterListAPIView(CachedListAPIView):
    # 脚部导航
    queryset = Nav.objects.filter(position=constants.NAV_FOOTER_POSITION,  is_show=True, is_deleted=False).order_by('order', '-id')[:constants.NAV_FOOTER_SIZE]
    serializer_class = NavSerializer


class BannerListAPIView(CachedListAPIView):
    # 轮播图
    queryset = Banner.objects.filter(is_show=True, is_deleted=False).order_by('order', '-id')[:constants.BANNER_SIZE]
    serializer_class = BannerSerializer