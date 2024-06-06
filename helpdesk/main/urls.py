from django.urls import path
from . import views # Импорт файла с методами вывода информации на экран views.py

# При открытии корневой страницы сайта выполнится метод
# views.index выводящий пользователю главную страницу сайта
urlpatterns = [
    path('', views.index),
    path('home', views.home, name='home'),
    path('requests', views.request_list, name='requests'),
    path('requests/new_request', views.create_request, name='new_request'),

    path('assets', views.assets, name='assets'),

    path('users', views.user_list, name='users'),
    path('profile', views.user_profile, name='user_profile'),
    path('users/new_user', views.register, name='new_user'),
    path('users/<int:pk>', views.UserProfileView.as_view(), name='user_details'),
    path('users/<int:pk>/update', views.UserProfileUpdate.as_view(), name='user_update'),
]