#  Создаем базу  данных
from django.db import models


#  Создаем базу  данных
class Card(models.Model):
    card_id = models.AutoField(primary_key=True, db_column='CardID')
    question = models.TextField(max_length=255, db_column='Question')
    answer = models.TextField(max_length=5000, db_column='Answer')
    category_id = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='cards',
                                    db_column='CategoryID')
    upload_date = models.DateTimeField(auto_now_add=True, db_column='UploadDate')
    views = models.IntegerField(default=0, db_column='Views')
    adds = models.IntegerField(default=0, db_column='Favorites')
    tags = models.ManyToManyField('Tag', related_name='cards', through='CardTag', )

    # конструкцию models.ManyToManyField , указывая параметр through для определения
    # промежуточной таблицы, которая управляет связью.

    class Meta:  # вьюшка
        db_table = 'Cards'  # имя таблицы
        verbose_name = 'Карточка'  # имя модели в единственном числе
        verbose_name_plural = 'Карточки'  # имя модели в множественном числе

    def __str__(self):
        return f'Карточка {self.question}-{self.answer[:50]}'


class Tag(models.Model):
    id = models.AutoField(primary_key=True, db_column='TagID')
    name = models.CharField(max_length=255, unique=True, db_column='Name')

    class Meta:
        db_table = 'Tags'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class CardTag(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    card = models.ForeignKey('Card', on_delete=models.CASCADE, db_column='CardID')
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, db_column='TagID')

    class Meta:
        db_table = 'CardTags'
        unique_together = ('card', 'tag')
        verbose_name = 'Тег карточки'
        verbose_name_plural = 'Теги карточек'

    def __str__(self):
        return f'{self.card} - {self.tag}'


class Category(models.Model):
    category_id = models.AutoField(primary_key=True, db_column='CategoryID')
    name = models.CharField(max_length=255, db_column='Name')

    class Meta:
        db_table = 'Categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

# python manage.py migrate
# python manage.py makemigrations - загрузили данные для миграции
# python manage.py migrate -fake
