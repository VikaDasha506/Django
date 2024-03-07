from django.shortcuts import render

info = {
    "users_count": 100500,
    "cards_count": 200600,
    "menu": ["Главная", "О проекте", "Каталог"]
}

# Create your views here.
from django.http import HttpResponse


# status = 200 - статус кода ответа (200 значит Все хорошо)
def main(request):  # делаем запрос
    return HttpResponse('Привет,мир!')  # вернет страничку с надписью


def card_detail(request, card_id):
    if card_id > 10:
        return HttpResponse(f'Такой карточки нет')
    return HttpResponse(f'Вы открыли карточку {card_id}')


def get_all_cards(request):
    """Принимает информацию о проекте info
    Возвращает по адресу"""
    return render(request, 'cards/catalog.html', context=info)
