from django import forms
from django.forms import inlineformset_factory
from .models import Post, Media
from django.forms import FileInput


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption']
        labels = {
            'caption': 'Описание'
        }






class MediaForm(forms.ModelForm):
    file = forms.ImageField(
        required=False,
        widget=FileInput(attrs={
            'class': 'file-input',
            'accept': 'image/*',
        })
    )

    class Meta:
        model = Media
        fields = ['file']

MediaFormSet = inlineformset_factory(
    Post,
    Media,
    form=MediaForm,   # <-- здесь передаём твою форму с FileInput
    fields=('file',),
    extra=1,          # сколько пустых полей показывать
    can_delete=False  # убираем кнопку "удалить"
)