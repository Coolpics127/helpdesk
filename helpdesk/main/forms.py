from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Profile, Jobs


class New_user_form(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите логин...'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите фамилию...'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите имя...'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all())
    is_active = forms.RadioSelect()

    class Meta:
        model = User
        fields = ('username','password1','password2','last_name','first_name','email','groups','is_active')


class New_user_profile_form(forms.ModelForm):
    patron = forms.CharField(label='Отчество', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите отчество...'}), required=False)
    job = forms.ModelChoiceField(empty_label='-------', queryset=Jobs.objects.all())
    phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-input'}), required=False)
    picture = forms.ImageField(label='Аватар', required=False)

    class Meta:
        model = Profile
        fields = ('patron','job','phone','picture')