from django.contrib.auth.models import User
from django.db import models
from django.core.validators import EmailValidator
import uuid


class Survey(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название опроса")
    description = models.TextField(verbose_name="Описание опроса", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class Question(models.Model):
    TEXT = 'text'
    SINGLE_CHOICE = 'single_choice'
    MULTIPLE_CHOICE = 'multiple_choice'

    QUESTION_TYPES = [
        (TEXT, 'Текстовый ответ'),
        (SINGLE_CHOICE, 'Один вариант ответа'),
        (MULTIPLE_CHOICE, 'Несколько вариантов ответа')
    ]

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(verbose_name="Текст вопроса")
    description = models.TextField(verbose_name="Описание", blank=True)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default=TEXT, verbose_name="Тип вопроса")
    is_required = models.BooleanField(default=True, verbose_name="Обязательный вопрос")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255, verbose_name="Текст варианта ответа")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'


class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses')
    response_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255, verbose_name="Имя")
    contact = models.CharField(max_length=255, verbose_name="Телефон или Telegram")
    location = models.CharField(max_length=255, verbose_name="Город или часовой пояс")
    email = models.EmailField(verbose_name="Email", validators=[EmailValidator()])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата прохождения")

    def __str__(self):
        return f"Ответ на опрос: {self.survey.title} (ID: {self.response_id})"

    class Meta:
        verbose_name = 'Ответ на опрос'
        verbose_name_plural = 'Ответы на опросы'


class QuestionResponse(models.Model):
    survey_response = models.ForeignKey(SurveyResponse, on_delete=models.CASCADE, related_name='question_responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')
    text_response = models.TextField(verbose_name="Текстовый ответ", blank=True)
    selected_choices = models.ManyToManyField(Choice, blank=True, related_name='responses')

    def __str__(self):
        return f"Ответ на вопрос: {self.question.text}"

    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопросы'


class ConsultationRequest(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name='Email', validators=[EmailValidator()])
    phone = models.CharField(max_length=100, verbose_name="Телефон или Telegram")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Отправлено")

    def __str__(self):
        return f"Request from {self.name} ({self.email})"

    class Meta:
        verbose_name = 'Заявка на консультацию'
        verbose_name_plural = 'Заявки на консультации'


class GrammarSection(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название раздела")
    description = models.TextField(verbose_name="Описание раздела", blank=True)
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Раздел грамматики'
        verbose_name_plural = 'Разделы грамматики'
        ordering = ['order', 'title']


class GrammarMaterial(models.Model):
    section = models.ForeignKey(GrammarSection, on_delete=models.CASCADE, related_name='materials',
                                verbose_name="Раздел")
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True)
    image = models.ImageField(upload_to='grammar_materials/', verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Грамматический материал'
        verbose_name_plural = 'Грамматические материалы'
        ordering = ['section', 'order', 'title']


class Homework(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True)
    image = models.ImageField(upload_to='homework/', verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_homework')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'
        ordering = ['-created_at']


class HomeworkSubmission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='homework_submissions')
    answer = models.TextField(verbose_name="Ответ")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")
    is_checked = models.BooleanField(default=False, verbose_name="Проверено")

    def __str__(self):
        return f"Ответ на {self.homework.title} от {self.user.username}"

    class Meta:
        verbose_name = 'Выполненное домашнее задание'
        verbose_name_plural = 'Выполненные домашние задания'
        ordering = ['-submitted_at']
