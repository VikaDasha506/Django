# from django.shortcuts import render

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
    return HttpResponse('Все карточки')
