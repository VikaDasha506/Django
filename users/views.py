from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegisterUserForm, LoginUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from cards.views import MenuMixin
from django.views.generic import TemplateView, CreateView


class LoginUser(MenuMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    extra_context = {'title': 'Авторизация'}
    redirect_field_name = 'next'

    def get_success_url(self):
        if self.request.POST.get('next', '').strip():
            return self.request.POST.get('next')
        return reverse_lazy('catalog')


class LogoutUser(MenuMixin, LogoutView):
    next_page = reverse_lazy('users:login')


class RegisterUser(CreateView):
    form_class = RegisterUserForm  # Указываем класс формы, который мы создали для регистрации
    template_name = 'register.html'  # Путь к шаблону, который будет использоваться для отображения формы
    extra_context = {'title': 'Регистрация'}  # Дополнительный контекст для передачи в шаблон
    success_url = reverse_lazy(
        'users:thanks')  # URL, на который будет перенаправлен пользователь после успешной регистрации

    def login_user(request):
        if request.method == 'POST':
            form = LoginUserForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    next_url = request.POST.get('next', '').strip()  # Получаем next или пустую строку
                    if next_url:  # Если next_url не пустой
                        return redirect(next_url)  # Перенаправляем на next_url
                    return redirect(reverse_lazy('catalog'))  # Перенаправляем на каталог, если next_url пуст
                else:
                    form.add_error(None, 'Неверное имя пользователя или пароль')
        else:
            form = LoginUserForm()
        return render(request, 'login.html', {'form': form})


class ThanksForRegister(MenuMixin, TemplateView):
    template_name = 'thanks.html'
    extra_context = {'title': 'Благодарим за регистрацию!'}
