from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import DateInput, DateTimeInput
from django.utils.translation import gettext_lazy as _


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя или Email', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Введите имя пользователя или Email'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-input', 'placeholder': 'Введите пароль'}))

    error_messages = {
        'invalid_login': _(
            "Пожалуйста, проверьте правильность введенных данных. "
            "Имя пользователя и пароль чувствительны к регистру."),
        'inactive': _("Этот аккаунт неактивен."),
    }


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя*', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Введите имя пользователя'}))
    email = forms.EmailField(label='Email*', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Введите ваш Email'}),
                             required=True)
    first_name = forms.CharField(label='Имя*', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Введите ваше имя'}),
                                 required=True)
    password1 = forms.CharField(label='Пароль*', widget=forms.PasswordInput(
        attrs={'class': 'form-input', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(label='Подтвердите пароль*', widget=forms.PasswordInput(
        attrs={'class': 'form-input', 'placeholder': 'Введите пароль еще раз'}))

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        labels = {
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
            'email': _('Email')
        }
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-input', 'placeholder': 'Введите ваше имя'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-input', 'placeholder': 'Введите вашу фамилию'}),
            'email': forms.TextInput(
                attrs={'class': 'form-input', 'placeholder': 'Введите ваш Email'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Удаляем поле 'usable_password', так как оно не требуется для регистрации
        if 'usable_password' in self.fields:
            del self.fields['usable_password']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с этим Email уже существует')
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Имя пользователя', widget=forms.TextInput(
        attrs={'class': 'form-input'}))
    email = forms.EmailField(disabled=True, label='Email', widget=forms.TextInput(
        attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']  # ,  'password1', 'password2']
        labels = {
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
        }
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-input'}),

        }
