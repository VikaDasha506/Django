from django.urls import path
from . import views
#cards/urls.py
# будет иметь префикс в urls.py
urlpatterns = [
    path('<int:card_id>/', views.card_detail, name='card_detail'),
    path('', views.get_all_cards, name='all_cards')
]