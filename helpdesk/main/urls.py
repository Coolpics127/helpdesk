from django.urls import path
from . import views # Импорт файла с методами вывода информации на экран views.py

# При открытии корневой страницы сайта выполнится метод
# views.index выводящий пользователю главную страницу сайта
urlpatterns = [
    path('', views.index),
    path('home', views.home, name='home'),
    path('requests', views.request_list, name='requests'),
    path('requests/new_request', views.create_request, name='new_request'),
    path('requests/<int:pk>',views.request_view, name='request_details'),
    path('assets', views.assets, name='assets'),
    path('assets/ip_list', views.ip_list, name='ip_list'),
    path('assets/logpass_list', views.logpasslist, name='logpass'),
    path('finances', views.supplies, name='finances'),
    path('knowledge', views.knoledge_base, name='knowledge'),
    path('users', views.user_list, name='users'),
    path('profile', views.user_profile, name='user_profile'),
    path('users/new_user', views.register, name='new_user'),
    path('users/<int:pk>', views.UserProfileView.as_view(), name='user_details'),
    path('users/<int:pk>/update', views.user_update, name='user_update'),
]