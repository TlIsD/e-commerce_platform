from django.urls import path, re_path
from .views import LoginAPIView, PhoneAPIView, UserAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    re_path(r'^phone/(?P<phone>1[3-9]\d{9})/$', PhoneAPIView.as_view()),
    path('register/', UserAPIView.as_view()),
]