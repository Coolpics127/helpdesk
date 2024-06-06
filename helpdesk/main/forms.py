from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Profile, Jobs, Requests, Priorities


class New_user_form(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите логин...'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Придумайте пароль...'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Повторите пароль...'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите фамилию...'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите имя...'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Введите email...'}))
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all())
    is_active = forms.RadioSelect()

    class Meta:
        model = User
        fields = ('username','password1','password2','last_name','first_name','email','groups','is_active')


class New_user_profile_form(forms.ModelForm):
    patron = forms.CharField(label='Отчество', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите отчество...'}), required=False)
    job = forms.ModelChoiceField(empty_label='-------', queryset=Jobs.objects.all())
    phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите телефон...'}), required=False)
    picture = forms.ImageField(label='Аватар', required=False)

    class Meta:
        model = Profile
        fields = ('patron', 'job', 'phone', 'picture')


class New_request(forms.ModelForm):
    request_date = forms.SplitHiddenDateTimeWidget()
    issued_by = forms.HiddenInput()
    request_name = forms.CharField(label='Название заявки', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите название заявки...'}))
    request_description = forms.CharField(label='Описание заявки', widget=forms.Textarea(attrs={'class': 'form-input'}))
    priority = forms.ModelChoiceField(label='Приоритет', empty_label='Установите приоритет', queryset=Priorities.objects.all(), required=False)
    desired_date = forms.DateField(label='Желаемая дата исполнения', widget=forms.DateInput(attrs={'class': 'form-input'}), required=False)
    attachment = forms.FileField(label='Прикрепленные объекты',widget=forms.FileInput(attrs={'class': 'form-input'}),required=False)

    class Meta:
        model = Requests
        fields = ('request_date','issued_by','request_name','request_description','priority','desired_date','attachment')