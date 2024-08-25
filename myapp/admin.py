from django.contrib import admin
from .models import Survey, Question, Choice, Response


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    verbose_name = 'Опрос'
    verbose_name_plural = 'Опросы'
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'survey', 'question_type')
    search_fields = ('text',)
    list_filter = ('survey', 'question_type')


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question')
    search_fields = ('text',)
    list_filter = ('question',)


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('question', 'text')
    search_fields = ('text',)
    list_filter = ('question',)
