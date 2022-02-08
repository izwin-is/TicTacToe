from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder':'Имя пользователя'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form__input', 'placeholder':'123456'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form__input', 'placeholder':'123456'}))
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form__input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form__input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form__input'})
        }

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class':'form__input'}))
    password = forms.CharField(label='Логин', widget=forms.PasswordInput(attrs={'class':'form__input'}))