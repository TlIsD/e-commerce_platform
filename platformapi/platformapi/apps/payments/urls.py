from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path("^alipay/(?P<order_number>[0-9]+)/$", views.AlipayAPIViewSet.as_view({"get":"link"})),
    path("alipay/result/", views.AlipayAPIViewSet.as_view({"get":"return_result"})),
    re_path("^alipay/query/(?P<order_number>[0-9]+)/$", views.AlipayAPIViewSet.as_view({"get":"query"})),
    path("alipay/notify/", views.AlipayAPIViewSet.as_view({"post": "notify_result"})),
]