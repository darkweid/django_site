# Generated by Django 5.1 on 2024-08-31 15:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_consultationrequest'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GrammarMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('image', models.ImageField(upload_to='grammar_materials/', verbose_name='Изображение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Грамматический материал',
                'verbose_name_plural': 'Грамматические материалы',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AlterModelOptions(
            name='consultationrequest',
            options={'verbose_name': 'Заявка на консультацию', 'verbose_name_plural': 'Заявки на консультации'},
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('image', models.ImageField(upload_to='homework/', verbose_name='Изображение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_homework', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Домашнее задание',
                'verbose_name_plural': 'Домашние задания',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='HomeworkSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(verbose_name='Ответ')),
                ('submitted_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')),
                ('is_checked', models.BooleanField(default=False, verbose_name='Проверено')),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='myapp.homework')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homework_submissions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Выполненное домашнее задание',
                'verbose_name_plural': 'Выполненные домашние задания',
                'ordering': ['-submitted_at'],
            },
        ),
    ]
