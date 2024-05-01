#  Создаем базу  данных
from django.db import models
from django import forms
from django.contrib.auth import get_user_model


#  Создаем базу  данных
class Card(models.Model):
    class Status(models.IntegerChoices):
        UNCHECKED = 0, 'Не проверено'
        CHECKED = 1, 'Проверено'

    card_id = models.AutoField(primary_key=True, db_column='CardID', verbose_name='ID')
    question = models.TextField(max_length=255, db_column='Question', verbose_name='Вопрос')
    answer = models.TextField(max_length=5000, db_column='Answer', verbose_name='Ответ')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='cards',
                                 db_column='CategoryID', verbose_name='Категория')
    upload_date = models.DateTimeField(auto_now_add=True, db_column='UploadDate', verbose_name='Дата загрузки')
    views = models.IntegerField(default=0, db_column='Views', verbose_name='Просмотры')
    adds = models.IntegerField(default=0, db_column='Favorites', verbose_name='Добавлено в избранное')
    tags = models.ManyToManyField('Tag', related_name='cards', through='CardTag', verbose_name='Просмотры')
    check_status = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]),
                                                         Status.choices)), default=Status.UNCHECKED,
                                       verbose_name='Статус проверки')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='cards', null=True,
                               default=None, verbose_name=('Автор'))

    # конструкцию models.ManyToManyField , указывая параметр through для определения
    # промежуточной таблицы, которая управляет связью.

    class Meta:  # вьюшка
        db_table = 'Cards'  # имя таблицы
        verbose_name = 'Карточка'  # имя модели в единственном числе.То что видно на сайте в админке
        verbose_name_plural = 'Карточки'  # имя модели в множественном числе.То что видно на сайте в админке

    def __str__(self):
        return f'Карточка: {self.question}-{self.answer[:50]}'  # То что видно на сайте в админке

    def get_absolute_url(self):
        return f'/cards/{self.card_id}/detail/'  # просмотр карточки с admin-> на сайте как она выглядет


class Tag(models.Model):
    id = models.AutoField(primary_key=True, db_column='TagID')
    name = models.CharField(max_length=255, unique=True, db_column='Name')

    class Meta:
        db_table = 'Tags'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'Тэг: {self.name}'


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
        return f'{self.tag} - {self.card}'


class Category(models.Model):
    category_id = models.AutoField(primary_key=True, db_column='CategoryID')
    name = models.CharField(max_length=255, db_column='Name')

    class Meta:
        db_table = 'Categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'Категория: {self.name}'


class CardModelForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ('question', 'answer', 'category', 'tags')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['tags'].queryset = Tag.objects.all()
        instance = super().save(commit=False)
        instance.save()
        self.instance.tags.clear()  # Очищаем текущие теги, чтобы избежать дублирования
        # Обрабатываем теги

