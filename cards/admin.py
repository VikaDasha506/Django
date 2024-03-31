from django.contrib import admin
from .models import Card

admin.site.register(Card)


#@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    pass
    # list_display = ('question', 'answer', 'upload_date', 'views', 'adds')

# http://127.0.0.1:8000/admin/
# логин Anna
# пароль admin
