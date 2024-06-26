from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.forms import ModelChoiceField

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

class User_edit_form(forms.ModelForm):
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите фамилию...'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите имя...'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Введите email...'}))
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all())
    is_active = forms.RadioSelect()
    class Meta:
        model = User
        fields = ('last_name','first_name','email','groups','is_active')

class New_user_profile_form(forms.ModelForm):
    patron = forms.CharField(label='Отчество', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите отчество...'}), required=False)
    job = forms.ModelChoiceField(empty_label='-------', queryset=Jobs.objects.all())
    phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите телефон...'}), required=False)
    picture = forms.ImageField(label='Аватар', required=False)

    class Meta:
        model = Profile
        fields = ('patron', 'job', 'phone', 'picture')

class User_profile_edit(forms.ModelForm):
    patron = forms.CharField(label='Отчество', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите отчество...'}), required=False)
    job = forms.ModelChoiceField(empty_label='-------', queryset=Jobs.objects.all())
    phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите телефон...'}), required=False)

    class Meta:
        model = Profile
        fields = ('patron', 'job', 'phone')

class ResponsibleChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()

class New_request(forms.ModelForm):
    issued_by = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    request_name = forms.CharField(label='Название заявки', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите название заявки...'}))
    request_description = forms.CharField(label='Описание заявки', widget=forms.Textarea(attrs={'class': 'form-input'}))
    responsible = ResponsibleChoiceField(label='Выберите исполнителя', empty_label='Исполнитель...', queryset=User.objects.filter(Q(groups='1') | Q(groups='2')), required=False, to_field_name="last_name")
    priority = forms.ModelChoiceField(label='Приоритет', empty_label='Приоритет...', queryset=Priorities.objects.all(), required=True)
    status = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    desired_date = forms.DateTimeField(label='Желаемая дата исполнения', widget=forms.DateTimeInput(attrs={'class': 'form-input'}),required=False)
    attachment = forms.FileField(label='Прикрепленные объекты',widget=forms.FileInput(attrs={'class': 'form-input'}),required=False)

    class Meta:
        model = Requests
        fields = ('issued_by','request_name','request_description','responsible','priority','status','desired_date','attachment')

class Request_response(forms.ModelForm):
    commentary = forms.CharField(label='Описание работ...', widget=forms.Textarea(attrs={'class': 'form-input'}),required=False)
    delete_commentary = forms.CharField(label='Описание причины...', widget=forms.Textarea(attrs={'class': 'form-input'}),required=False)
    revision_commentary = forms.CharField(label='Описание проверки...', widget=forms.Textarea(attrs={'class': 'form-input'}),required=False)
    responce_attachments = forms.FileField(label='Прикрепленные объекты',widget=forms.FileInput(attrs={'class': 'form-input'}),required=False)
    date_completed = forms.DateTimeField(label='Дата исполнения', widget=forms.DateTimeInput(attrs={'class': 'form-input'}), required=False)

    class Meta:
        model = Requests
        fields = ('commentary','delete_commentary','revision_commentary','responce_attachments','date_completed')