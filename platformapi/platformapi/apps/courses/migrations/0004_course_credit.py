# Generated by Django 3.2.9 on 2025-05-07 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_alter_course_course_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='credit',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='积分'),
        ),
    ]
