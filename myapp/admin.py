from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import (Survey, Question, Choice, SurveyResponse, QuestionResponse,
                     ConsultationRequest, GrammarMaterial,
                     Homework, HomeworkSubmission, GrammarSection)


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'view_responses_link')
    search_fields = ('title',)
    list_filter = ('created_at',)

    def view_responses_link(self, obj):
        url = reverse('admin_survey_responses', args=[obj.id])
        return format_html('<a href="{}">Просмотр ответов</a>', url)

    view_responses_link.short_description = "Ответы"


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'survey', 'question_type', 'is_required')
    search_fields = ('text',)
    list_filter = ('survey', 'question_type', 'is_required')


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question')
    search_fields = ('text',)
    list_filter = ('question',)


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ('survey', 'name', 'email', 'contact', 'location', 'created_at', 'response_id')
    search_fields = ('name', 'email', 'contact', 'location', 'response_id')
    list_filter = ('survey', 'created_at')
    readonly_fields = ('response_id',)


@admin.register(QuestionResponse)
class QuestionResponseAdmin(admin.ModelAdmin):
    list_display = ('survey_response', 'question', 'text_response')
    search_fields = ('text_response',)
    list_filter = ('question', 'survey_response__survey')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('survey_response', 'question')

    def survey_response(self, obj):
        return obj.survey_response.response_id

    survey_response.short_description = 'Survey Response ID'


@admin.register(ConsultationRequest)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at', 'message')
    search_fields = ('name',)
    list_filter = ('created_at',)

    def view_responses_link(self, obj):
        url = reverse('admin_survey_responses', args=[obj.id])
        return format_html('<a href="{}">Просмотр заявок</a>', url)

    view_responses_link.short_description = "Ответы"


@admin.register(GrammarSection)
class GrammarSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    search_fields = ('title', 'description')
    list_editable = ('order',)


@admin.register(GrammarMaterial)
class GrammarMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'order', 'created_at')
    list_filter = ('section', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('order', 'section')


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_image', 'assigned_to', 'created_at')
    search_fields = ('title', 'description', 'assigned_to__username')
    list_filter = ('created_at', 'assigned_to')

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}"height="200" />', obj.image.url)
        return "Нет изображения"

    display_image.short_description = 'Изображение'


@admin.register(HomeworkSubmission)
class HomeworkSubmissionAdmin(admin.ModelAdmin):
    list_display = ('homework_card', 'user', 'submitted_at', 'is_checked', 'answer_preview')
    search_fields = ('homework__title', 'user__username')
    list_filter = ('submitted_at', 'is_checked', 'homework', 'user')
    readonly_fields = ('submitted_at', 'homework_image')
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'homework')
        }),
        ('Задание', {
            'fields': ('homework_image',)
        }),
        ('Ответ', {
            'fields': ('answer', 'is_checked')
        }),
        ('Мета-информация', {
            'fields': ('submitted_at',)
        }),
    )

    def homework_card(self, obj):
        homework = obj.homework
        return format_html(
            '<div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px;">'
            '<h3>{}</h3>'
            '<p>{}</p>'
            '{}'
            '</div>',
            homework.title,
            homework.description,
            format_html('<img src="{}" style="max-width: 400px; max-height: 200px;" />',
                        homework.image.url) if homework.image else ''
        )

    homework_card.short_description = 'Карточка задания'

    def answer_preview(self, obj):
        return obj.answer[:100] + '...' if len(obj.answer) > 100 else obj.answer

    answer_preview.short_description = 'Ответ'

    def homework_image(self, obj):
        homework = obj.homework
        if homework.image:
            return format_html('<img src="{}" style="width: 700px;" />', homework.image.url)
        return 'Нет изображения'

    homework_image.short_description = 'Изображение задания'

    def mark_as_checked(self, request, queryset):
        queryset.update(is_checked=True)

    mark_as_checked.short_description = "Отметить выбранные задания как проверенные"

    actions = [mark_as_checked]
