from django.urls import path
from . import views

urlpatterns = [
    path("", views.CouponListAPIView.as_view()),
    path("enable/", views.EnableCouponListAPIView.as_view()),
]