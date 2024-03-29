from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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

@login_required
def user_list(request):
    return render(request, 'main/user_list.html')