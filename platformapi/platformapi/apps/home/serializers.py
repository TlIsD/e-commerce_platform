from rest_framework import serializers
from .models import Nav, Banner


class NavSerializer(serializers.ModelSerializer):
    # 导航序列化器
    class Meta:
        model = Nav
        fields = ['name', 'link', 'is_http']

class BannerSerializer(serializers.ModelSerializer):
    # 轮播图序列化器
    class Meta:
        model = Banner
        fields = ['name', 'link', 'is_http', 'image']