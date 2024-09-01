# Generated by Django 5.1 on 2024-09-01 09:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_alter_homeworksubmission_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='homeworksubmission',
            options={'ordering': ['-submitted_at'], 'verbose_name': 'Выполненное домашнее задание', 'verbose_name_plural': 'Выполненные домашние задания'},
        ),
        migrations.RemoveField(
            model_name='homeworksubmission',
            name='checked_answer',
        ),
        migrations.AlterField(
            model_name='homeworksubmission',
            name='homework',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='myapp.homework'),
        ),
        migrations.AlterField(
            model_name='homeworksubmission',
            name='is_checked',
            field=models.BooleanField(default=False, verbose_name='Проверено'),
        ),
        migrations.AlterField(
            model_name='homeworksubmission',
            name='submitted_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки'),
        ),
        migrations.AlterField(
            model_name='homeworksubmission',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homework_submissions', to=settings.AUTH_USER_MODEL),
        ),
    ]
