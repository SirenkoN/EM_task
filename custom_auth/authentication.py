import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class JWTAuthentication(BaseAuthentication):
    """
    При каждом запросе читаем заголовок Authorization:
        Bearer <jwt_token>
    Декодируем токен, получаем user_id и ищем пользователя в БД.
    Если пользователь не найден или inactive → 401.
    """

    def authenticate(self, request):
        header = request.headers.get('Authorization')
        if not header or not header.startswith('Bearer '):
            return None  # Django будет использовать fallback auth

        token = header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.JWT_SECRET,
                                algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Срок действия токена истек.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Недействительный токен.')

        user_id = payload.get('user_id')
        if not user_id:
            raise AuthenticationFailed('Отсутствует идентификатор пользователя .')

        try:
            from custom_auth.models import User
            user = User.objects.get(id=user_id, is_active=True)
        except User.DoesNotExist:
            raise AuthenticationFailed('Пользователь не найден или неактивен.')
        return (user, None)  # request.user будет установлен
