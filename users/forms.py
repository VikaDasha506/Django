from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import datetime


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterUserForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = get_user_model()  # Используем текущую модель пользователя
        fields = (
            'username', 'email', 'first_name', 'password1', 'password2')  # Обратите внимание на изменение полей пароля
        labels = {
            'email': 'E-Mail',
            'first_name': 'Имя'
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError('Такой email уже существует.')  # Проверка уникальности email
        return email


class ProfileUserForm(forms.ModelForm):
    this_year = datetime.date.today().year
    date_birth = forms.DateField(
        label='Дата рождения',
        widget=forms.SelectDateWidget(years=range(this_year - 100, this_year - 5)),
        required=False
    )
    photo = forms.ImageField(
        label='Фотография',
        required=False
    )

    username = forms.CharField(
        disabled=True,  # Поле не редактируемое
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control'})  # Использование Bootstrap класса
    )
    email = forms.CharField(
        disabled=True,  # Поле не редактируемое
        label='E-mail',
        widget=forms.TextInput(attrs={'class': 'form-control'})  # Использование Bootstrap класса
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'date_birth', 'photo']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'date_birth': 'Дата рождения',
            'photo': 'Фотография'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'})
        }


class UserPasswordChangeForm(PasswordChangeForm):
    """класс формы для смены пароля"""
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Старый пароль'}))
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Новый пароль'}))
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтверждение нового пароля'}))


