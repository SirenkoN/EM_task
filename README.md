# Система Аутентификации и Авторизации

## Описание проекта

Реализована собственная система аутентификации (регистрация, login, logout)  
и авторизации (разграничение доступа к ресурсам).  

## Технологический стек

- Django 4.x
- Django REST Framework (DRF)
- PostgreSQL
- Django's built-in password hashing
- `PyJWT` – генерация JWT токенов

## Схема БД

| Таблица | Поля |
|---------|------|
| **roles** | id, name (`admin`, `manager`, `user`) |
| **business_elements** | id, name (users, products, orders) |
| **access_rules** | id, role_id, element_id, <br> `read_permission`, `read_all_permission`,<br>`create_permission`, `update_permission`, `update_all_permission`,<br>`delete_permission`, `delete_all_permission` |

Все поля с суффиксом `_permission` – булевы (`True/False`).  
Права могут быть «всем» (`*_all_permission`) или только собственным объектам (предполагается наличие поля `owner_id` в бизнес‑таблицах).

## API

### Пользовательские эндпоинты

- **POST `/api/register/`** – регистрация
- **POST `/api/login/`** – вход, выдача JWT
- **GET `/api/profile/`** – получение профиля (пользователя)
- **PATCH `/api/profile/`** – обновление данных
- **DELETE `/api/profile/`** – мягкое удаление (`is_active=False`)
- **POST `/api/logout/`** – выход

### Правила доступа

- **GET `/api/rules/`** – список всех правил (admin)
- **POST `/api/rules/`** – добавить правило
- **PATCH `/api/rules/<id>/`** – изменить правило

При каждом запросе к бизнес‑объекту проверяется токен -> пользователь, его роль -> соответствующее правило.  
Ответы:

| Статус | Описание |
|--------|----------|
| 401 Unauthorized | Пользователь не аутентифицирован (нет токена) |
| 403 Forbidden | Пользователь найден, но права отсутствуют |

### Мок‑объекты

- **GET `/business/products/`** – список продуктов (если пользователь имеет `read_permission` или `read_all_permission` для `products`)
- **GET `/business/orders/`** – список заказов
- **GET `/business/users/`** – список пользователей

## Как запустить проект

```bash
git clone <repo>
cd project
pip install -r requirements.txt
cp .env.example .env
# Заполните .env значениями
python manage.py makemigrations custom_auth
python manage.py migrate
# Заполнение базы данными
python manage.py loaddata project/fixtures/roles.json project/fixtures/business_elements.json project/fixtures/access_rules.json
# Создание суперпользователя
python manage.py createsuperuser
python manage.py runserver
