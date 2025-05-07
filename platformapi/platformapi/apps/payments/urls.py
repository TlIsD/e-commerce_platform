from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path("^alipay/(?P<order_number>[0-9]+)/$", views.AlipayAPIViewSet.as_view({"get":"link"})),
]