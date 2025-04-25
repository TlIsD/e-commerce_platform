import random

from django.core.management.base import BaseCommand, CommandError
from apps.courses.models import Teacher
from faker import Faker

class Command(BaseCommand):
    # 类名必须是Command且一个文件就是一个命令类, 必须继承BaseCommand
    help = '添加课程相关测试数据'

    # 如果该命令要接受来自终端的参数, 可以使用add_arguments
    def add_arguments(self, parser):
        # 位置参数, 必填
        # parser.add_argument('name', nargs='+', type=int)

        # 命令参数, 选填
        parser.add_argument('--type', dest='type', default='teacher', type=str, help='测试数据的类型')

        parser.add_argument('--number', dest='number', default=10, type=int, help='添加数据的数量')

    def handle(self, *args, **options):
        # 添加测试数据
        if options['type'] == 'teacher':
            self.add_teacher(options)
        elif options['type'] == 'direction':
            self.add_direction(options)

    def add_teacher(self, options):
        # 添加教师的测试数据
        faker = Faker(['zh_CN'])
        for i in range(options['number']):
            Teacher.objects.create(
                # 姓名唯一
                name=faker.unique.name(),
                avatar='teacher/default.jpg',
                role=random.randint(0, 2),
                title='老师',
                signature= '从业多年，经验丰富',
                brief=f'联系电话：{faker.unique.phone_number()}',
            )
        print('添加教师测试数据完毕')

    def add_direction(self, options):
        # 添加学习方向测试数据
        print('添加学习方向测试数据完毕')