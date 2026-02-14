"""Представления приложения custom_auth."""

from datetime import timedelta

from django.utils import timezone
from rest_framework import generics, status, viewsets, permissions
from rest_framework.response import Response

from .models import User, AccessRule
from .serializers import UserSerializer, AccessRuleSerializer, LoginSerializer

import jwt
from django.conf import settings

class IsAdminRole(permissions.BasePermission):
    """Проверяет, является ли пользователь администратором."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role
            and request.user.role.name == "Admin"
        )

class RegisterView(generics.CreateAPIView):
    """Регистрация нового пользователя.

    Доступно без аутентификации.
    Автоматически назначает роль 'User'.
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    """Получить, обновить или удалить профиль текущего пользователя.

    При удалении выполняется мягкое удаление (is_active=False).
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        """Возвращает текущего аутентифицированного пользователя."""
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        """Мягкое удаление аккаунта.

        Args:
            request: HTTP-запрос

        Returns:
            Response: Пустой ответ с кодом 204
        """
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginView(generics.GenericAPIView):
    """Вход по email и паролю.

    Возвращает JWT-токен для последующих запросов.
    """

    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Аутентифицирует пользователя и возвращает JWT токен.

        Args:
            request: HTTP-запрос с данными email и password

        Returns:
            Response: Токен в случае успеха

        Status Codes:
            200: Успешная аутентификация
            400: Некорректные данные
            401: Неправильные учетные данные
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        try:
            user = User.objects.get(email=data["email"])
            if not user.is_active:
                return Response(
                    {"detail": "Account is inactive."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.check_password(data["password"]):
            return Response(
                {"detail": "Incorrect password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Создаем JWT с правильным форматом временных меток
        now = timezone.now()
        exp = int((now + timedelta(hours=1)).timestamp())
        iat = int(now.timestamp())

        token = jwt.encode(
            {"user_id": user.id, "exp": exp, "iat": iat},
            settings.JWT_SECRET,
            algorithm="HS256",
        )
        return Response({"token": token})


class LogoutView(generics.GenericAPIView):
    """Выход из системы.

    Технически, клиент должен удалить токен на своей стороне.
    """

    def post(self, request):
        """Обрабатывает запрос на выход.

        Args:
            request: HTTP-запрос

        Returns:
            Response: Пустой ответ с кодом 200
        """
        return Response(status=status.HTTP_200_OK)


class RuleViewSet(viewsets.ModelViewSet):
    """CRUD для правил доступа.

    Доступно только администраторам.
    """

    queryset = AccessRule.objects.all()
    serializer_class = AccessRuleSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]


