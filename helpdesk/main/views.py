from django.shortcuts import render

# Метод, который открывает (рендерит) страницу index.html
def index(request):
    return render(request, 'main/index.html')