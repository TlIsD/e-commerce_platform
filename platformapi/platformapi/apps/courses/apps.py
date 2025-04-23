from django.apps import AppConfig


class CourseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'courses'
    verbose_name = '课程管理'
    verbose_name_plural = verbose_name