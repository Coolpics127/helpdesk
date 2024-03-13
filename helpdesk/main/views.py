from django.shortcuts import render

# Метод, который открывает (рендерит) страницу index.html
def index(request):
    return render(request, 'main/index.html')

# Метод, который открывает (рендерит) страницу с заявками req_page.html
def request_list(request):
    return render(request, 'main/req_page.html')

def user_list(request):
    return render(request, 'main/user_list.html')