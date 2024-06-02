from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import New_user_form, New_user_profile_form


def index(request):
    return render(request, 'main/index.html')

# Метод, который открывает (рендерит) страницу home.html
@login_required
def home(request):
    return render(request, 'main/home.html')

# Метод, который открывает (рендерит) страницу с заявками req_page.html
@login_required
def request_list(request):
    return render(request, 'main/req_page.html')

# Метод, который открывает страницу списка пользователей
@login_required
def user_list(request):
    users = get_user_model().objects.all()
    return render(request, 'main/user_list.html', {'users':users})

# Метод, который открывает страницу профиля пользователя
@login_required
def user_profile(request):
    return render(request,'main/profile.html')

@login_required
def register(request):
    if request.method == 'POST':
        user_form = New_user_form(request.POST)
        profile_form = New_user_profile_form(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            #form1.save()
            #username = form1.cleaned_data.get('username')
            user = user_form.save()
            profile = profile_form.save(commit = False)
            profile.user = user
            profile.save()
            return redirect('users')
    else:
        user_form = New_user_form()
        profile_form = New_user_profile_form()
    return render(request, 'main/new_user_2.html', {'user_form': user_form, 'profile_form': profile_form})