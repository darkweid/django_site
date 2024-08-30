from django.urls import path, re_path, register_converter
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('explore-topics/', views.explore_topics, name='explore-topics'),
    path('contact/', views.contact, name='contact'),
    path('reviews/', views.reviews, name='reviews'),
    path('questionnaire/', views.questionnaire, name='questionnaire'),
    path('lk/', views.lk, name='lk'),
    path('survey-thank-you/', views.survey_thank_you, name='survey_thank_you'),  # Страница успешной отправки
    path('admin/survey/<int:survey_id>/responses/', views.survey_responses_view, name='admin_survey_responses'),
    path('submit-request/', views.submit_request, name='submit_request'),

]
