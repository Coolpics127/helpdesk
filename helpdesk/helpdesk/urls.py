from django.contrib import admin
from django.urls import path, include # include необходимо подключить для ссылания на файлы urls.py внутри приложений

# Библиотеки для поддержки статических файлов
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account_app.urls')),
    path('', include('main.urls')), # При открытии корневого каталога сайта ссылка обрабатывается в файле main.urls
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Подключение статических файлов (стилей css, картинок и т.д.)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
