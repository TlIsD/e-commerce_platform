from django.urls import path, re_path

from .views import LoginAPIView, PhoneAPIView, UserAPIView, SmsCodeAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    # re_path(r'^phone_login/(?P<phone>1[3-9]\d{9})/$', PhoneLoginAPIView.as_view()),

    re_path(r'^phone/(?P<phone>1[3-9]\d{9})/$', PhoneAPIView.as_view()),
    path('register/', UserAPIView.as_view()),
    re_path(r'^code/(?P<phone>1[3-9]\d{9})/$', SmsCodeAPIView.as_view()),
]