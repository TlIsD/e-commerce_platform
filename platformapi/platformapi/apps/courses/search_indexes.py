from haystack import indexes
from .models import Course

class CourseIndex(indexes.SearchIndex, indexes.Indexable):
    # 全文索引
    text = indexes.CharField(document=True, use_template=True)

    # 普通索引
    id = indexes.IntegerField(model_attr="id")
    name = indexes.CharField(model_attr="name")
    description = indexes.CharField(model_attr="description")
    teacher = indexes.CharField(model_attr="teacher__name")
    course_cover = indexes.CharField(model_attr="course_cover")
    get_level_display = indexes.CharField(model_attr="get_level_display")
    students = indexes.IntegerField(model_attr="students")
    get_status_display = indexes.CharField(model_attr="get_status_display")
    lessons = indexes.IntegerField(model_attr="lessons")
    pub_lessons = indexes.IntegerField(model_attr="pub_lessons")
    price = indexes.DecimalField(model_attr="price")
    credit = indexes.IntegerField(model_attr="credit")
    discount = indexes.CharField(model_attr="discount_json")
    order = indexes.IntegerField(model_attr="order")

    # 指定与当前es索引模型对接的mysql的ORM模型
    def get_model(self):
        return Course

    # 当用户搜索es索引时，对应的提供的mysql数据集
    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_deleted=False, is_show=True)