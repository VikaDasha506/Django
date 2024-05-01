"""
get_all_cards - возвращает все карточки для представления в каталоге
get_categories - возвращает все категории для представления в каталоге
get_cards_by_category - возвращает карточки по категории для представления в каталоге
get_cards_by_tag - возвращает карточки по тегу для представления в каталоге
get_detail_card_by_id - возвращает детальную информацию по карточке для представления

"""

from django.db.models import F, Q
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from .models import Card
from django.views.decorators.cache import cache_page
from django.shortcuts import render
from .forms import CardModelForm#, RegisterUserForm
from django.views.generic.list import ListView
from django.views.generic import TemplateView, DetailView
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


info = {
    "users_count": 100500,
    "cards_count": 200600,
    # "menu": ['Главная', 'О проекте', 'Каталог']
    "menu": [
        {"title": "Главная",
         "url": "/",
         "url_name": "index"},
        {"title": "О проекте",
         "url": "/about/",
         "url_name": "about"},
        {"title": "Каталог",
         "url": "/cards/catalog/",
         "url_name": "catalog"},
    ],
}


class MenuMixin:
    """Класс-миксин для добавления меню в контекст шаблона
    Добывает и кеширует cards_count, users_count, menu"""
    timeout = 30  # устанавливает время жизни кеша в секундах.

    def get_menu(self):
        """получает меню из кеша, если оно доступно, иначе получает его из базы данных и кеширует его."""
        menu = cache.get('menu')
        if not menu:
            menu = info['menu']
            cache.set('menu', menu, timeout=self.timeout)
        return menu

    def get_cards_count(self):
        """получает количество карточек из кеша, если оно доступно,
        иначе считает количество карточек в базе данных и кеширует его."""
        cards_count = cache.get('cards_count')
        if not cards_count:
            cards_count = Card.objects.count()
            cache.set('cards_count', cards_count, timeout=self.timeout)
        return cards_count

    def get_users_count(self):
        """получает количество пользователей из кеша,
        если оно доступно, иначе считает количество пользователей в базе данных и кеширует его."""
        users_count = cache.get('users_count')
        if not users_count:
            users_count = get_user_model().objects.count()
            cache.set('users_count', users_count, timeout=self.timeout)
        return users_count

    def get_context_data(self, **kwargs):
        """вызывает методы get_menu(), get_cards_count() и get_users_count(),
        и добавляет полученные значения в контекст шаблона."""
        context = super().get_context_data(**kwargs)
        context['menu'] = self.get_menu()
        context['cards_count'] = self.get_cards_count()
        context['users_count'] = self.get_users_count()
        return context


class AboutView(MenuMixin, TemplateView):
    """Вьюшка для статики. Но можно при желании добавить динамический контент"""
    template_name = 'about.html'
    extra_context = {'title': 'О проекте'}  # Обновляется только при загрузке Сервера


class IndexView(MenuMixin, TemplateView):
    """наследует от MenuMixin и TemplateView.
     Oсновная страница. Шаблон 'main.html'."""
    template_name = 'main.html'


class PageNotFoundView(MenuMixin, TemplateView):
    """Наследует от MenuMixin и TemplateView.
     Страница ошибки 404. Шаблон '404.html'."""
    template_name = '404.html'


@cache_page(60 * 15)
def catalog(request):
    """Функция для отображения страницы "Каталог"
    будет возвращать рендер шаблона /templates/cards/catalog.html
    - **`sort`** - ключ для указания типа сортировки с возможными значениями: `date`, `views`, `adds`.
    - **`order`** - опциональный ключ для указания направления сортировки с возможными значениями: `asc`, `desc`. По умолчанию `desc`.
    """
    # Считываем параметры из GET запроса
    sort = request.GET.get('sort', 'upload_date')  # по умолчанию сортируем по дате загрузки
    order = request.GET.get('order', 'desc')  # по умолчанию используем убывающий порядок
    search_query = request.GET.get('search_query', '')  # поиск по карточкам
    page_number = request.GET.get('page', 1)  # номер страницы
    # Сопоставляем параметр сортировки с полями модели
    valid_sort_fields = {'upload_date', 'views', 'adds'}
    if sort not in valid_sort_fields:
        sort = 'upload_date'
    # Обрабатываем порядок сортировки
    if order == 'asc':
        order_by = sort
    else:
        order_by = f'-{sort}'
    # Если человек ничего не искал
    if not search_query:
        # Получаем карточки из БД в ЖАДНОМ режиме многие ко многим tags
        cards = Card.objects.select_related('category').prefetch_related('tags').order_by(order_by)
    # Если человек что-то искал
    else:
        cards = Card.objects.filter(Q(question__icontains=search_query) | Q(answer__icontains=search_query) | Q(
            tags__name__icontains=search_query)).select_related('category').prefetch_related('tags').order_by(
            order_by).distinct()
    # Создаем объект пагинатора и передаем ему карточки и количество карточек на странице
    paginator = Paginator(cards, 25)
    # Получаем объект страницы
    page_obj = paginator.get_page(page_number)
    # Подготавливаем контекст и отображаем шаблон
    context = {
        'cards': cards,
        'cards_count': len(cards),
        'menu': info['menu'],
        'page_obj': page_obj,
        "sort": sort,  # Передаем, для того чтобы при переходе по страницам сохранялся порядок сортировки
        "order": order,  # Аналогично
    }

    response = render(request, 'cards/catalog.html', context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # - кэш не используется
    response['Expires'] = '0'  # Перестраховка - устаревание кэша
    return response


class CatalogView(MenuMixin, ListView):
    model = Card  # Указываем модель, данные которой мы хотим отобразить
    template_name = 'cards/catalog.html'  # Путь к шаблону, который будет использоваться для отображения страницы
    context_object_name = 'cards'  # Имя переменной контекста, которую будем использовать в шаблоне
    paginate_by = 30  # Количество объектов на странице

    # Метод для модификации начального запроса к БД
    def get_queryset(self):
        # Получение параметров сортировки из GET-запроса
        sort = self.request.GET.get('sort', 'upload_date')
        order = self.request.GET.get('order', 'desc')
        search_query = self.request.GET.get('search_query', '')

        # Определение направления сортировки
        if order == 'asc':
            order_by = sort
        else:
            order_by = f'-{sort}'

        # Фильтрация карточек по поисковому запросу и сортировка
        if search_query:
            queryset = Card.objects.filter(
                Q(question__iregex=search_query) |
                Q(answer__iregex=search_query) |
                Q(tags__name__iregex=search_query)
            ).select_related('category').prefetch_related('tags').order_by(order_by).distinct()
        else:
            queryset = Card.objects.select_related('category').prefetch_related('tags').order_by(order_by)
        return queryset

    # Метод для добавления дополнительного контекста
    def get_context_data(self, **kwargs):
        # Получение существующего контекста из базового класса
        context = super().get_context_data(**kwargs)
        # Добавление дополнительных данных в контекст
        context['sort'] = self.request.GET.get('sort', 'upload_date')
        context['order'] = self.request.GET.get('order', 'desc')
        context['search_query'] = self.request.GET.get('search_query', '')
        return context


def get_categories(request):
    """
    Возвращает все категории для представления в каталоге
    """
    return HttpResponse('All categories')


def get_cards_by_category(request, slug):
    """
    Возвращает карточки по категории для представления в каталоге
    """
    return HttpResponse(f'Cards by category {slug}')


def get_cards_by_tag(request, tag_id):
    """Возвращает карточки по тегу для представления в каталоге"""
    cards = Card.objects.filter(tags__id=tag_id)
    context = {
        'cards': cards,
        'cards_count': cards.count(),
        'menu': info['menu']
    }
    return render(request, 'cards/catalog.html', context)


@cache_page(60 * 15)  # Кэширует на 15 минут
def get_cards_by_tag(request, tag_id):
    """
    Возвращает карточки по тегу для представления в каталоге
    Мы используем многие-ко-многим, получая все карточки, которые связаны с тегом
    Временно, мы будем использовать шаблон каталога
    """
    # cards = Card.objects.filter(tags=tag_id)

    # Жадная загрузка
    cards = Card.objects.filter(tags=tag_id).prefetch_related('tags')
    context = {
        'cards': cards,
        'cards_count': cards.count(),
        'menu': info['menu'],
    }
    return render(request, 'cards/catalog.html', context)


class CardDetailView(MenuMixin, DetailView):
    model = Card  # Указываем, что моделью для этого представления является Card
    template_name = 'cards/card_detail.html'  # Указываем путь к шаблону для детального отображения карточки
    context_object_name = 'card'  # Переопределяем имя переменной в контексте шаблона на 'card'

    # Метод для обновления счетчика просмотров при каждом отображении детальной страницы карточки
    def get_object(self, queryset=None):
        # Получаем объект с учетом переданных в URL параметров (в данном случае, pk или id карточки)
        obj = super().get_object(queryset=queryset)
        # Увеличиваем счетчик просмотров на 1 с помощью F-выражения для избежания гонки условий
        Card.objects.filter(pk=obj.pk).update(views=F('views') + 1)
        return obj


class CardUpdateView(LoginRequiredMixin, UpdateView):
    model = Card  # Указываем модель, с которой работает представление
    form_class = CardModelForm  # Указываем класс формы для создания карточки
    template_name = 'cards/add_card.html'  # Указываем шаблон, который будет использоваться для отображения формы
    redirect_field_name = 'next'  # Имя GET-параметра, в котором хранится URL для перенаправления после входа

    # После успешного обновления карточки, пользователь будет перенаправлен на страницу этой карточки
    def get_success_url(self):
        return reverse_lazy('detail_card_by_id', kwargs={'pk': self.object.pk})


def preview_card_ajax(request):
    """принимает запрос request и проверяет его метод.
    Если метод равен "POST", функция извлекает question, answer, category из запроса."""
    if request.method == "POST":
        question = request.POST.get('question', '')
        answer = request.POST.get('answer', '')
        category = request.POST.get('category', '')
        # Генерация HTML для предварительного просмотра
        html_content = render_to_string('cards/card_detail.html', {
            'card': {
                'question': question,
                'answer': answer,
                'category': 'Тестовая категория',
                'tags': ['тест', 'тег'],

            }
        }
                                        )

        return JsonResponse({'html': html_content})
    return JsonResponse({'error': 'Invalid request'}, status=400)


class AddCardCreateView(LoginRequiredMixin, MenuMixin, CreateView):
    model = Card  # Указываем модель, с которой работает представление
    form_class = CardModelForm  # Указываем класс формы для создания карточки
    template_name = 'cards/add_card.html'  # Указываем шаблон, который будет использоваться для отображения формы
    success_url = reverse_lazy('catalog')  # URL для перенаправления после успешного создания карточки
    login_url = reverse_lazy(
        'users:login')  # указываем  URL для входа в систему, который будет использоваться для перенаправления пользователя на страницу аутентификации.
    redirect_field_name = 'next'  # имя параметра запроса, в котором хранится URL-адрес, на который пользователь должен быть перенаправлен после успешного входа в систему.


class EditCardUpdateView(MenuMixin, UpdateView):
    model = Card  # Указываем модель, с которой работает представление
    form_class = CardModelForm  # Указываем класс формы для редактирования карточки
    template_name = 'cards/add_card.html'  # Указываем шаблон, который будет использоваться для отображения формы
    context_object_name = 'card'  # Имя переменной контекста для карточки
    success_url = reverse_lazy('catalog')  # URL для перенаправления после успешного редактирования карточки


class CardDeleteView(DeleteView):
    model = Card  # Указываем модель, с которой работает представление
    success_url = reverse_lazy('catalog')  # URL для перенаправления после успешного удаления карточки
    template_name = 'cards/delete_card.html'  # Указываем шаблон, который будет использоваться для отображения формы подтверждения удаления
