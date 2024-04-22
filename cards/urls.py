from django.urls import path
from . import views

# ссылка на дет.представ.картоыки /cards/2/detail/
urlpatterns = [
    path('catalog/', views.CatalogView.as_view(), name='catalog'),  # Общий каталог всех карточек
    path('categories/', views.get_categories, name='categories'),  # Список всех категорий
    path('categories/<slug:slug>/', views.get_cards_by_category, name='category'),  # Карточки по категории
    path('tags/<int:tag_id>/', views.get_cards_by_tag, name='cards_by_tag'),# новый маршрут для просмотра карточек по тегу
    path('<int:pk>/detail/', views.CardDetailView.as_view(), name='detail_card_by_id'),# Детальное отображение карточки
    path('<int:pk>/edit/', views.CardUpdateView.as_view(), name='edit_card'),  # Редактирование карточки
    path('<int:pk>/delete/', views.CardDeleteView.as_view(), name='delete_card'),# Удаление карточки
    path('add/', views.AddCardCreateView.as_view(), name='add_card'),  # добавление карточек в форме CardForm
    path('preview_card_ajax/', views.preview_card_ajax, name='preview_card_ajax'),
]
