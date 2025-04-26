from django.urls import path, re_path
from . import views

urlpatterns = [
    path('directions/', views.CourseDirectionListAPIView.as_view()),
    re_path(r'categories/(?P<direction>\d+)/', views.CourseCategoryListAPIView.as_view()),
    re_path(r"^(?P<direction>\d+)/(?P<category>\d+)/$", views.CourseListAPIView.as_view()),
]