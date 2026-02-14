# Базовый образ Python
FROM python:3.12-slim

# Устанавливаем рабочий каталог внутри контейнера
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . .

# Устанавливаем зависимости из requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Открываем порт, который Django слушает по умолчанию
EXPOSE 8000

# Команда для запуска миграций и запуска сервера
CMD ["sh", "-c", "python manage.py migrate --no-input && python manage.py loaddata project/fixtures/roles.json project/fixtures/business_elements.json project/fixtures/access_rules.json && python manage.py runserver 0.0.0.0:8000"]

