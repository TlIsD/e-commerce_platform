from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.OrderCreateAPIView.as_view()),
    path("pay/choices/", views.OrderPayChoicesAPIView.as_view()),
    path("list/", views.OrderListAPIView.as_view()),
    re_path("^(?P<pk>\d+)/$", views.OrderViewSet.as_view({"put": "pay_cancel"})),
]