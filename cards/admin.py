from django.contrib import admin
from .models import Card, Category, Tag, CardTag
from django.contrib.admin import SimpleListFilter


# http://127.0.0.1:8000/admin/
# логин Anna
# пароль admin

# admin.site.register(Card)
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    # поля,отображаемые в админке
    list_display = ('card_id', 'question', 'answer', 'category', 'views', 'adds', 'upload_date', 'check_status')
    list_display_links = ('question', 'category')  # кликабельные поля
    search_fields = ('question', 'answer')  # поиск по вопросу и ответу
    list_filter = ('category', 'check_status')  # добавим фильтр для категорий
    ordering = ('-upload_date', 'card_id')  # сортировка
    list_per_page = 25  # количество элементов на странице
    list_editable = ('check_status',)  # поля,которые можно редактировать
    actions = ['make_checked', 'make_unchecked']
    change_form_template = 'admin/cards/change_form.html'

    @admin.action(description='Отметить выбранные карточки как проверенные')
    def make_checked(self, request, queryset):
        queryset.update(check_status=True)

    @admin.action(description='Отметить выбранные карточки как непроверенные')
    def make_unchecked(self, request, queryset):
        queryset.update(check_status=False)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(CardTag)
class CardTagAdmin(admin.ModelAdmin):
    pass
