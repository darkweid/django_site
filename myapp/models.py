from django.db import models


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
    text = models.CharField(max_length=255, verbose_name="Текст вопроса")
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default=TEXT, verbose_name="Тип вопроса")

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


class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')
    text = models.TextField(verbose_name="Ответ пользователя", blank=True)
    selected_choices = models.ManyToManyField(Choice, blank=True, related_name='responses')

    def __str__(self):
        return f"Ответ на вопрос: {self.question.text}"

    class Meta:
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователей'
