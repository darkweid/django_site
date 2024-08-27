from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Survey, Question, Choice, SurveyResponse, QuestionResponse, ConsultationRequest


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
    list_display = ('name', 'email','phone', 'created_at', 'message')
    search_fields = ('name',)
    list_filter = ('created_at',)

    def view_responses_link(self, obj):
        url = reverse('admin_survey_responses', args=[obj.id])
        return format_html('<a href="{}">Просмотр заявок</a>', url)

    view_responses_link.short_description = "Ответы"