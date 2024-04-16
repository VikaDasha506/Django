"""
get_all_cards - возвращает все карточки для представления в каталоге
get_categories - возвращает все категории для представления в каталоге
get_cards_by_category - возвращает карточки по категории для представления в каталоге
get_cards_by_tag - возвращает карточки по тегу для представления в каталоге
get_detail_card_by_id - возвращает детальную информацию по карточке для представления

"""
from django.db.models import F, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from cards.models import Card
from .forms import CardModelForm, UploadFileForm
import os

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


def main(request):
    """Представление рендерит шаблон base.html"""
    return render(request, 'main.html', context=info)


def about(request):
    cards = Card.objects.all()
    context = {
        'cards': cards,
        'cards_count': len(cards),
        'menu': info['menu'],
        'users_count': info['users_count']
    }
    """Представление рендерит шаблон about.html"""
    return render(request, 'about.html', context)


def get_all_cards(request):
    """Возвращает все карточки для представления в каталоге"""
    sort = request.GET.get('sort', 'views')  # либо по ключу sort,если нет sort сортировка будет по upload_date
    order = request.GET.get('order', 'desc')  # либо по ключу order,если нет sort сортировка будет по desc
    search_query = request.GET.get('search_query','')
    page_number = None
    valid_sort_fields = {'upload_date', 'views', 'adds'}
    if sort not in valid_sort_fields:
        sort = 'views'
    if order == 'asc':
        order_by = sort
    else:
        order_by = f'-{sort}'

    if not search_query:
        cards = Card.objects.select_related('category').prefetch_related('tags').order_by(order_by)
    else:
        cards = Card.objects.filter(
                Q(question__icontains=search_query) |
                Q(answer__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct().order_by(order_by)

    context = {
        'cards': cards,
        'cards_count': len(cards),
        'menu': info['menu'],
    }

    return render(request, 'cards/catalog.html', context)


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


def get_detail_card_by_id(request, card_id):
    """Возвращает детальную информацию по карточке для представления"""
    # Ищем карточку по id в нашем наборе данных
    card = get_object_or_404(Card, pk=card_id)  # - вывод ошибки,если нет карточки с таким ид
    card.views = F('views') + 1  # добавили колличество просмотров
    card.save()  # сохранили изменение с кол-ом просмотров
    card.refresh_from_db()  # обновляем данные в таблице
    context = {
        'card': card,
        'menu': info['menu'],
    }

    return render(request, 'cards/card_detail.html', context)


def add_card(request):
    if request.method == 'POST':
        form = CardModelForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            answer = form.cleaned_data['answer']
            category = form.cleaned_data['category']
            card = Card(question=question, answer=answer, category=category)
            card.save()
            # получили id созданной карточки
            card_id = card.card_id
            return HttpResponseRedirect(f'/cards/{card_id}/detail')
    else:
        form = CardModelForm()
    return render(request, 'cards/add_card.html', {'form': form, 'menu': info['menu']})


def handle_uploaded_file(f):
    # Создаем путь к файлу в директории uploads, имя файла берем из объекта f
    file_path = f'uploads/{f.name}'

    # Создаем папку uploads, если ее нет
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Открываем файл для записи в бинарном режиме (wb+)
    with open(file_path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return file_path


def add_card_by_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Записываем файл на диск
            file_path = handle_uploaded_file(request.FILES['file'])
            # Редирект на страницу каталога после успешного сохранения
            return redirect('catalog')
    else:
        form = UploadFileForm()
    return render(request, 'cards/add_file_card.html', {'form': form})
