"""Модели приложения custom_auth."""

from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Менеджер для работы с кастомной моделью пользователя."""

    def create_user(self, email, password=None, **extra_fields):
        """Создает и сохраняет обычного пользователя.

        Args:
            email: Email пользователя
            password: Пароль (может быть None для временных пользователей)
            **extra_fields: Дополнительные поля пользователя

        Returns:
            User: Созданный пользователь

        Raises:
            ValueError: Если не указан email
        """
        if not email:
            raise ValueError("Укажите email")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создает и сохраняет суперпользователя.

        Args:
            email: Email администратора
            password: Пароль
            **extra_fields: Дополнительные поля

        Returns:
            User: Созданный суперпользователь

        Raises:
            ValueError: Если не установлены флаги is_staff или is_superuser
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Убедимся, что роль Admin существует
        admin_role, _ = Role.objects.get_or_create(name="Admin")
        extra_fields.setdefault("role", admin_role)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Суперпользователь должен иметь is_superuser=True."
            )

        return self.create_user(email, password, **extra_fields)


class Role(models.Model):
    """Модель ролей пользователей (admin, manager, user)."""

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self):
        """Возвращает название роли."""
        return self.name


class User(AbstractBaseUser):
    """Кастомная модель пользователя, заменяющая стандартную User."""

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)

    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, related_name="users"
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        """Возвращает строковое представление пользователя."""
        return f"{self.first_name} {self.last_name} ({self.email})"

    def has_perm(self, perm, obj=None):
        """Проверяет права пользователя.

        Для суперпользователя всегда возвращает True.

        Args:
            perm: Строка с правом
            obj: Объект, к которому применяется право

        Returns:
            bool: Наличие прав
        """
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Проверяет права доступа к модулю.

        Для суперпользователя всегда возвращает True.

        Args:
            app_label: Название приложения

        Returns:
            bool: Наличие прав
        """
        return self.is_superuser


class BusinessElement(models.Model):
    """Модель бизнес-элементов системы (users, products, orders)."""

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Business Element"
        verbose_name_plural = "Business Elements"

    def __str__(self):
        """Возвращает название бизнес-элемента."""
        return self.name


class AccessRule(models.Model):
    """Модель правил доступа к бизнес-элементам.

    Связывает роль, элемент системы и набор разрешений.
    """

    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name="access_rules"
    )
    element = models.ForeignKey(
        BusinessElement, on_delete=models.CASCADE, related_name="access_rules"
    )

    read_permission = models.BooleanField(default=False)
    read_all_permission = models.BooleanField(default=False)
    create_permission = models.BooleanField(default=False)
    update_permission = models.BooleanField(default=False)
    update_all_permission = models.BooleanField(default=False)
    delete_permission = models.BooleanField(default=False)
    delete_all_permission = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Access Rule"
        verbose_name_plural = "Access Rules"
        unique_together = ("role", "element")

    def __str__(self):
        """Возвращает описание правила доступа."""
        return f"{self.role} → {self.element}"


