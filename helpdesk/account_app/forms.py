from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'username_field'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'password_field'}))
