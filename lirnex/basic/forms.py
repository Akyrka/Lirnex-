from django import forms
from django.forms import inlineformset_factory
from .models import Post, Media

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption']



MediaFormSet = inlineformset_factory(
    Post,
    Media,
    fields=('file',),   # поле в модели Media
    extra=1,            # сколько пустых полей показывать по умолчанию
)



