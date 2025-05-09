from django.urls import path, re_path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
# 注册全文搜索到视图集中生成url路由信息
router.register('search', views.CourseSearchView, basename='course-search')

urlpatterns = [
    path('directions/', views.CourseDirectionListAPIView.as_view()),
    re_path(r'categories/(?P<direction>\d+)/', views.CourseCategoryListAPIView.as_view()),
    re_path(r"^(?P<direction>\d+)/(?P<category>\d+)/$", views.CourseListAPIView.as_view()),
    path('hotword/', views.HotWordAAPIView.as_view()),
    re_path('^(?P<pk>\d+)/$', views.CourseRetrieveAPIView.as_view()),
    re_path("^(?P<course>\d+)/chapters/$", views.CourseChapterListAPIView.as_view()),
    path("type/", views.CourseTypeListAPIView.as_view()),
] + router.urls