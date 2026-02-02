from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import bcrypt

# --------------------------------------------------------------------
# Роли пользователей (admin, manager, user)
# --------------------------------------------------------------------
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# --------------------------------------------------------------------
# Пользователь – собственный пользовательский класс
# --------------------------------------------------------------------
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)          # логин
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)

    password_hash = models.TextField()            # хеш пароля

    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)  # роль пользователя
    is_active = models.BooleanField(default=True)   # мягкое удаление

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def set_password(self, raw_password):
        """Хешируем пароль и сохраняем в password_hash."""
        self.password_hash = bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, raw_password):
        """Сверяем введённый пароль с хешем."""
        return bcrypt.checkpw(raw_password.encode(), self.password_hash.encode())

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


# --------------------------------------------------------------------
# Бизнес‑элементы (users, products, orders)
# --------------------------------------------------------------------
class BusinessElement(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# --------------------------------------------------------------------
# Правила доступа: роль -> элемент -> права
# --------------------------------------------------------------------
class AccessRule(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    element = models.ForeignKey(BusinessElement, on_delete=models.CASCADE)

    # Права (bool). Если True – пользователь может делать действие со *всеми* объектами.
    read_permission = models.BooleanField(default=False)
    read_all_permission = models.BooleanField(default=False)
    create_permission = models.BooleanField(default=False)
    update_permission = models.BooleanField(default=False)
    update_all_permission = models.BooleanField(default=False)
    delete_permission = models.BooleanField(default=False)
    delete_all_permission = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.role} → {self.element}"
