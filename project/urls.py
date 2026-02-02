from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),                     # Django админка
    path('api/', include('custom_auth.urls')),           # API аутентификации и авторизации
    path('business/', include('business.urls')),         # мок‑объекты бизнес‑приложения
]
