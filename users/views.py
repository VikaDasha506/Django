from django.contrib.auth import get_user_model
from .forms import RegisterUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from cards.views import MenuMixin
from django.views.generic import TemplateView, CreateView, ListView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileUserForm, UserPasswordChangeForm
from cards.models import Card


class LoginUser(MenuMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}
    redirect_field_name = 'next'

    def get_success_url(self):
        if self.request.POST.get('next', '').strip():
            return self.request.POST.get('next')
        return reverse_lazy('catalog')


class LogoutUser(MenuMixin, LogoutView):
    next_page = reverse_lazy('users:login')


class RegisterUser(MenuMixin, CreateView):
    form_class = RegisterUserForm  # Указываем класс формы, который мы создали для регистрации
    template_name = 'users/register.html'  # Путь к шаблону, который будет использоваться для отображения формы
    extra_context = {'title': 'Регистрация'}  # Дополнительный контекст для передачи в шаблон
    success_url = reverse_lazy(
        'users:thanks')  # URL, на который будет перенаправлен пользователь после успешной регистрации


class ThanksForRegister(MenuMixin, TemplateView):
    template_name = 'users/thanks.html'
    extra_context = {'title': 'Благодарим за регистрацию!'}


class ProfileUser(MenuMixin, LoginRequiredMixin, UpdateView):
    model = get_user_model()  # Используем модель текущего пользователя
    form_class = ProfileUserForm  # Связываем с формой профиля пользователя
    template_name = 'users/profile.html'  # Указываем путь к шаблону
    extra_context = {'title': 'Профиль пользователя',
                     'active_tab': 'profile'}  # Дополнительный контекст для передачи в шаблон

    def get_success_url(self):
        # URL, на который переадресуется пользователь после успешного обновления
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        # Возвращает объект модели, который должен быть отредактирован
        return self.request.user


class PasswordChange(MenuMixin, PasswordChangeView):
    """Класс для смены пароля аутентифицированного пользователя.
    Смена пароля"""
    template_name = 'users/password_change_form.html'  # путь к шаблону фоомы смены пароля
    form_class = UserPasswordChangeForm  # класс формы для смены пароля
    extra_context = {'title': 'Смена пароля',
                     # Словарь с дополнительным контекстом, например `{'title': 'Смена пароля'}`
                     'active_tab': 'password_change'}
    success_url = reverse_lazy(
        'users:password_change_done')  # `reverse_lazy` для указания URL-адреса перенаправления после успешной смены пароля

    def form_valid(self, form):
        # Метод, вызываемый при успешной валидации формы.
        # Может быть переопределен для добавления дополнительной логики
        return super().form_valid(form)


class PasswordChangeDone(MenuMixin, TemplateView):
    """Отображает страницу об успешном изменении пароля.
    Подтверждение смены пароля"""
    template_name = 'users/password_change_done.html'  # путь к шаблону страницы, подтверждающей успешное изменение пароля
    extra_context = {
        'title': 'Пароль успешно изменен'}  # Словарь с дополнительным контекстом, например `{'title': 'Пароль успешно изменен'}


class UserCardsView(MenuMixin, ListView):
    model = Card
    template_name = 'users/profile_cards.html'
    context_object_name = 'cards'
    extra_context = {'title': 'Мои карточки',
                     'active_tab': 'profile_cards'}

    def get_queryset(self):
        return Card.objects.filter(author=self.request.user).order_by('-upload_date')

