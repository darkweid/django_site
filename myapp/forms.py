from django import forms
from .models import SurveyResponse, Question
from django.utils.safestring import mark_safe


class SurveyForm(forms.ModelForm):
    class Meta:
        model = SurveyResponse
        fields = ['name', 'contact', 'location', 'email']

    def __init__(self, *args, **kwargs):
        survey = kwargs.pop('survey')
        super(SurveyForm, self).__init__(*args, **kwargs)

        for question in survey.questions.all():
            field_name = f'question_{question.id}'
            if question.question_type == Question.TEXT:
                widget = QuestionWithDescriptionWidget(question=question)
                self.fields[field_name] = forms.CharField(
                    label='',
                    widget=widget,
                    required=question.is_required
                )
            elif question.question_type == Question.SINGLE_CHOICE:
                widget = CustomRadioSelect(question=question)
                choices = [(choice.id, choice.text) for choice in question.choices.all()]
                self.fields[field_name] = forms.ChoiceField(
                    label='',
                    choices=choices,
                    widget=widget,
                    required=question.is_required
                )
            elif question.question_type == Question.MULTIPLE_CHOICE:
                widget = CustomCheckboxSelectMultiple(question=question)
                choices = [(choice.id, choice.text) for choice in question.choices.all()]
                self.fields[field_name] = forms.MultipleChoiceField(
                    label='',
                    choices=choices,
                    widget=widget,
                    required=question.is_required
                )


class QuestionWithDescriptionWidget(forms.Textarea):
    def __init__(self, question, *args, **kwargs):
        self.question = question
        attrs = kwargs.get('attrs', {})
        attrs['class'] = attrs.get('class', '') + ' custom-textarea'
        kwargs['attrs'] = attrs
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        question_text = f"<div class='question-block'><span class='question-text'>{self.question.text}</span><br>"
        description_text = f"<small class='question-description'>{self.question.description}</small><br>" if self.question.description else ""
        input_html = super().render(name, value, attrs, renderer)
        return mark_safe(f"{question_text}{description_text}{input_html}</div>")


class CustomRadioSelect(forms.RadioSelect):
    def __init__(self, question, *args, **kwargs):
        self.question = question
        attrs = kwargs.get('attrs', {})
        attrs['class'] = attrs.get('class', '') + ' custom-radio-select'
        kwargs['attrs'] = attrs
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        question_text = f"<div class='question-block'><span class='question-text'>{self.question.text}</span><br>"
        description_text = f"<small class='question-description'>{self.question.description}</small><br>" if self.question.description else ""
        html = super().render(name, value, attrs, renderer)
        return mark_safe(f"{question_text}{description_text}{html}</div>")


class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def __init__(self, question, *args, **kwargs):
        self.question = question
        attrs = kwargs.get('attrs', {})
        attrs['class'] = attrs.get('class', '') + ' custom-checkbox-select'
        kwargs['attrs'] = attrs
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        question_text = f"<div class='question-block'><span class='question-text'>{self.question.text}</span><br>"
        description_text = f"<small class='question-description'>{self.question.description}</small><br>" if self.question.description else ""
        html = super().render(name, value, attrs, renderer)
        return mark_safe(f"{question_text}{description_text}{html}</div>")
