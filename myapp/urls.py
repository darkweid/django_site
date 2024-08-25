from django.urls import path, re_path, register_converter
from . import views



urlpatterns = [
    path('', views.index, name='home'),  # http://127.0.0.1:8000
    path('explore-topics/', views.explore_topics, name='explore-topics'),
    path('contact/', views.contact, name='contact'),
    path('reviews/', views.reviews, name='reviews'),
    path('questionnaire/', views.questionnaire, name='questionnaire'),
    path('login/', views.login, name='login'),
    path('submit_form/', views.submit_form, name='submit_form'),
    path('success/', views.success_page, name='success_page'),  # Страница успешной отправки

    # path('cats/<int:cat_id>/', views.categories, name='cats_id'), # http://127.0.0.1:8000/cats/2/
    # path('cats/<slug:cat_slug>/', views.categories_by_slug, name='cats'),  # http://127.0.0.1:8000/cats/fdgdg/
]
