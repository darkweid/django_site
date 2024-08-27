from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import SurveyForm
from .models import Survey, SurveyResponse, QuestionResponse, Question, ConsultationRequest

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

def questionnaire(request, survey_id=1):
    survey = get_object_or_404(Survey, id=survey_id)

    if request.method == 'POST':
        form = SurveyForm(request.POST, survey=survey)
        if form.is_valid():
            survey_response = form.save(commit=False)
            survey_response.survey = survey
            survey_response.save()

            for question in survey.questions.all():
                field_name = f'question_{question.id}'
                if field_name in form.cleaned_data:
                    response = QuestionResponse(
                        survey_response=survey_response,
                        question=question
                    )
                    if question.question_type == Question.TEXT:
                        response.text_response = form.cleaned_data[field_name]
                    else:
                        response.save()  # Сохраняем перед добавлением many-to-many
                        selected_choices = form.cleaned_data[field_name]
                        if not isinstance(selected_choices, list):
                            selected_choices = [selected_choices]
                        response.selected_choices.set(selected_choices)
                    response.save()

            return redirect('survey_thank_you')
    else:
        form = SurveyForm(survey=survey)

    return render(request, 'myapp/survey.html', {'form': form, 'survey': survey})


def login(request):
    data = {'title': 'Личный кабинет'}
    return render(request, 'myapp/login.html', context=data)


def survey_thank_you(request):
    return HttpResponse('Good')



@staff_member_required
def survey_responses_view(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    responses = SurveyResponse.objects.filter(survey=survey).order_by('-created_at')

    return render(request, 'admin/survey_responses.html', {
        'survey': survey,
        'responses': responses,
    })

def submit_request(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        # Создание новой заявки
        ConsultationRequest.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )

        # Возврат успешного ответа
        return JsonResponse({"message": "Спасибо, что оставили заявку, я свяжусь с вами в ближайшее время!"})

    return JsonResponse({"message": "Ошибка при отправке заявки."}, status=400)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Ошибка 404 <br><br>Страница не найдена</h1>")
