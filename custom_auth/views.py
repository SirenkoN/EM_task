from rest_framework import generics, viewsets, status, permissions
from .serializers import UserSerializer, RoleSerializer, BusinessElementSerializer, AccessRuleSerializer
from .models import User, Role, BusinessElement, AccessRule

# ------------------- ПОЛЬЗОВАТЕЛЬ ---------------------------------

class RegisterView(generics.CreateAPIView):
    """Регистрация нового пользователя."""
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # открыто


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    """Получить/обновить профиль, удалить аккаунт (soft)."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)

    def destroy(self, request, *args, **kwargs):
        """Мягкое удаление – is_active=False + logout."""
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginView(generics.GenericAPIView):
    """Вход по email и паролю – выдаём JWT."""
    serializer_class = UserSerializer  # используем для входа, но не сохраняем

    def post(self, request):
        data = request.data
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(data['password']):
            return Response({'detail': 'Incorrect password.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        # Создаём JWT
        token = jwt.encode({'user_id': user.id}, settings.JWT_SECRET,
                           algorithm='HS256')
        return Response({'token': token})


class LogoutView(generics.GenericAPIView):
    """Logout – просто очистка токена на клиенте."""
    def post(self, request):
        # На клиенте можно удалить cookie/token
        return Response(status=status.HTTP_200_OK)


# ------------------- АДМИН ИЗМЕНЕНИЕ ПРАВ ---------------------------------

class RuleViewSet(viewsets.ModelViewSet):
    """CRUD для правил доступа (admin only)."""
    queryset = AccessRule.objects.all()
    serializer_class = AccessRuleSerializer
    permission_classes = [permissions.IsAdminUser]  # только админ
