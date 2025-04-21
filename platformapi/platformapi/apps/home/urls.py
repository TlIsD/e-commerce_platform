from django.urls import path
from . import views

urlpatterns = [
    path('nav/header/', views.NavHeaderListAPIView.as_view()),
    path('nav/footer/', views.NavFooterListAPIView.as_view()),
    path('banner/', views.BannerListAPIView.as_view()),
]