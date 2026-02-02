# Базовый образ Python (допустим Python 3.13)
FROM python:3.13-slim

# Устанавливаем рабочий каталог внутри контейнера
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . .

# Устанавливаем зависимости из requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Открываем порт, который Django слушает по умолчанию
EXPOSE 8000

# Запускаем сервер Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
