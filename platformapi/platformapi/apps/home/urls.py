from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.HomeAPIView.as_view()),
]