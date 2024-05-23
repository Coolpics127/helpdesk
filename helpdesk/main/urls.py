from django.urls import path
from . import views # Импорт файла с методами вывода информации на экран views.py

# При открытии корневой страницы сайта выполнится метод
# views.index выводящий пользователю главную страницу сайта
urlpatterns = [
    path('', views.index),
    path('home', views.home, name='home'),
    path('request', views.request_list, name='request'),
    path('users', views.user_list, name='users'),
    path('profile', views.user_profile, name='user_profile'),
]