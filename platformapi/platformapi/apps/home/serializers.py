from rest_framework import serializers
from .models import Nav

class NavSerializer(serializers.ModelSerializer):
    # 导航序列化器
    class Meta:
        model = Nav
        fields = ['name', 'link', 'is_http']