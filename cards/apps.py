from django.apps import AppConfig


class CardsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cards'
    verbose_name = 'Карточка'  # имя модели в единственном числе.То что видно на сайте в админке
    verbose_name_plural = 'Карточки'  # имя модели в множественном числе.То что видно на сайте в админке
