# Generated by Django 5.1 on 2024-08-26 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_choice_options_alter_question_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.CharField(max_length=600, verbose_name='Текст вопроса'),
        ),
    ]
