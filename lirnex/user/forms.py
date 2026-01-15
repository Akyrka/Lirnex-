from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile 
from django.forms.widgets import DateInput, FileInput

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Имя')
    last_name = forms.CharField(max_length=30, required=True, help_text='Фамилия')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    # Используем обычный FileInput без чекбокса Clear
    photo_profile = forms.ImageField(
        required=False,
        widget=FileInput(attrs={'class': 'file-input'})
    )

    class Meta:
        model = Profile
        fields = ['photo_profile', 'bio', 'birthday']
        widgets = {
            'bio': forms.Textarea(attrs={
                'placeholder': 'Напиши щось про себе...',
                'rows': 3,
                'style': 'width:100%; padding:8px;'
            }),
            'birthday': DateInput(attrs={
                'type': 'date',
                'style': 'padding:5px;'
            }),
        }
