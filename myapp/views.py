from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Survey

menu = [{'title': 'Про меня', 'url_name': 'about'},
        {'title': 'Контакты', 'url_name': 'contact'},
        {'title': 'Отзывы', 'url_name': 'reviews'},
        {'title': 'Заполнить тестовое задание', 'url_name': 'test'},
        {'title': 'Личный кабинет', 'url_name': 'login'}
        ]


def index(request):
    data = {'title': 'Главная страница'}
    return render(request, 'myapp/index.html', context=data)


def explore_topics(request):
    data = {'title': 'Как я работаю'}
    return render(request, 'myapp/explore_topics.html', context=data)


def contact(request):
    data = {'title': 'Связаться со мной'}
    return render(request, 'myapp/contact.html', context=data)


def reviews(request):
    data = {'title': 'Отзывы'}
    return render(request, 'myapp/reviews.html', context=data)


def questionnaire(request):
    survey = Survey.objects.get(id=1)
    context = {
        'title': 'Questionnaire',
        'survey': survey,
    }
    return render(request, 'myapp/survey.html', context)


def login(request):
    data = {'title': 'Личный кабинет'}
    return render(request, 'myapp/login.html', context=data)


def success_page(request):
    return HttpResponse('Good')


def submit_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Здесь можно добавить логику для обработки данных, например, сохранение в базе данных или отправку email

        return redirect(reverse('success_page'))  # Перенаправление на страницу успеха после отправки формы

    return render(request, 'form_page.html', {'title': 'Заполните форму'})


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Ошибка 404 <br><br>Страница не найдена</h1>")
