from django import forms
from .models import Category, Card, Tag


class CardModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CardModelForm, self).__init__(*args, **kwargs)
    question = forms.CharField(label='Вопрос', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}))  # label - создает лейбл рядом с полем
    answer = forms.CharField(label='Ответ', max_length=5000, widget=forms.Textarea(
        attrs={'rows': 5, 'cols': 40, 'class': 'form-control'}))  # Textarea- поле для ввода большого текста
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория',
                                      empty_label="Категория не выбрана", widget=forms.Select(
            attrs={'class': 'form-control'}))
    # required=False-делает не обязательным,empty_label-пустой лэйбл с надписью Категория не выбрана
    tags = forms.CharField(label='Теги', required=False, help_text='Перечислите теги через запятую',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Card  # Указываем модель, с которой работает форма
        # Указываем, какие поля должны присутствовать в форме и в каком порядке
        fields = ['question', 'answer', 'category', 'tags']
        # Указываем виджеты для полей
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 40}),
        }
        # Указываем метки для полей
        labels = {
            'question': 'Вопрос',
            'answer': 'Ответ',
        }

    def clean_tags(self):
        tags_str = self.cleaned_data['tags'].lower()
        tag_list = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        return tag_list

    def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        instance.save()
        for tag_name in self.cleaned_data['tags']:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            instance.tags.add(tag)

        return instance


class UploadFileForm(forms.Form):
    file = forms.FileField(label='Выберите файл', widget=forms.FileInput(attrs={'class': 'form-control'}))
