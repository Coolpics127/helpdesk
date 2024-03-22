from django.urls import path
from . import views # Импорт файла с методами вывода информации на экран views.py

urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]