import os
from pathlib import Path

# Путь к корню проекта (директория, содержащая manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------
# Секретный ключ и режим отладки
# --------------------------------------------------------------------
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# --------------------------------------------------------------------
# База данных PostgreSQL (параметры берутся из переменных окружения)
# --------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'auth_db'),
        'USER': os.getenv('DB_USER', 'user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# --------------------------------------------------------------------
# Список установленных приложений
# --------------------------------------------------------------------
INSTALLED_APPS = [
    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',            # встроенное приложение для auth_user_model
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third‑party
    'rest_framework',
    'corsheaders',

    # Наши приложения – обновлённый путь
    'custom_auth',
    'business',
]

# --------------------------------------------------------------------
# Middleware
# --------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS (если нужен)
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --------------------------------------------------------------------
# Основной URL конфиг
# --------------------------------------------------------------------
ROOT_URLCONF = 'project.urls'

# --------------------------------------------------------------------
# Шаблоны (не нужны для API, но оставляем)
# --------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# --------------------------------------------------------------------
# WSGI и ASGI
# --------------------------------------------------------------------
WSGI_APPLICATION = 'project.wsgi.application'
ASGI_APPLICATION = 'project.asgi.application'

# --------------------------------------------------------------------
# Настройки DRF
# --------------------------------------------------------------------
REST_FRAMEWORK = {
    # По умолчанию используем наш JWT‑auth класс
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'custom_auth.authentication.JWTAuthentication',
    ),
    # По умолчанию требуем авторизацию (401 если не логин)
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# --------------------------------------------------------------------
# CORS (если нужен, открываем все источники)
# --------------------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = True

# --------------------------------------------------------------------
# Статические файлы
# --------------------------------------------------------------------
STATIC_URL = '/static/'

# --------------------------------------------------------------------
# Переопределяем модель пользователя
# --------------------------------------------------------------------
AUTH_USER_MODEL = 'custom_auth.User'
