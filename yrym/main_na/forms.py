from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,Posts
from django.forms import ModelForm, TextInput, FileInput
from django import forms

class ProfileUpdateForm(ModelForm):
    """
    Форма обновления данных профиля пользователя
    """
    class Meta:
        model = Profile
        fields = ('bio', 'contacts', 'jenres', 'avatar')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы обновления
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

class UserUpdateForm(ModelForm):
    """
    Форма обновления данных пользователя
    """

    class Meta:
        model = User
        fields = ('username', 'first_name')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы обновления
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    def clean_email(self):
        """
        Проверка email на уникальность
        """
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email адрес должен быть уникальным')
        return email

class PostsForm(ModelForm):

    class Meta:
        model = Posts
        fields= ['title','desc','cover','audiofile']
        widgets={
             'title': TextInput(attrs={
                 'class':'form-control form-control-lg',
                 'placeholder': 'Название'
             }),
             'desc': TextInput(attrs={
                 'class': 'form-control form-control-lg',
                 'placeholder': 'Описание'
             }),
            'cover': FileInput(attrs={
                'class': 'form-control',
                'type':'file',
                'id':'CoverInput'
            }),
            'audiofile':FileInput(attrs={
                'class': 'form-control',
                'type': 'file',
                'id': 'AudioInput',
                'accept': '.mp3'
            })

        }