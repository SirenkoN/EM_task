"""Модуль аутентификации с использованием JWT."""

import jwt
from django.conf import settings
from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class JWTAuthentication(BaseAuthentication):
    """
    Аутентификация с использованием JWT.

    Проверяет заголовок Authorization: Bearer <jwt_token>.
    Декодирует токен и ищет пользователя в БД.

    Важно: Исключает проверку для эндпоинтов /register/ и /login/,
    так как они используются для получения токена.
    """

    def authenticate(self, request):
        """
        Аутентифицирует запрос, используя JWT.

        Возвращает кортеж (user, None) при успешной аутентификации.
        Возвращает None для открытых эндпоинтов.
        Вызывает AuthenticationFailed при ошибках валидации.

        Args:
            request: HTTP-запрос

        Returns:
            Tuple[User, None]: аутентифицированный пользователь и None
            None: если запрос к открытому эндпоинту

        Raises:
            AuthenticationFailed: если токен недействителен или устарел
        """
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None  # Пропускаем для дальнейшей обработки

        # Пропускаем проверку токена для открытых эндпоинтов
        if request.path.endswith('/register/') or request.path.endswith('/login/'):
            return None

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET, algorithms=["HS256"], options={"verify_exp": True}
            )
        except jwt.ExpiredSignatureError as e:
            raise AuthenticationFailed("Срок действия токена истек.") from e
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed("Недействительный токен.") from e

        user_id = payload.get("user_id")
        if not user_id:
            raise AuthenticationFailed("Отсутствует идентификатор пользователя.")

        try:
            from custom_auth.models import User

            user = User.objects.get(id=user_id, is_active=True)
        except User.DoesNotExist as e:
            raise AuthenticationFailed(
                "Пользователь не найден или неактивен."
            ) from e

        return (user, None)

