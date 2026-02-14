"""Сериализаторы для приложения custom_auth."""

from rest_framework import serializers

from .models import User, Role, BusinessElement, AccessRule


class LoginSerializer(serializers.Serializer):
    """Сериализатор для аутентификации пользователя."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        """Пропускает атрибуты без проверки.

        Фактическая проверка учетных данных происходит в представлении LoginView.

        Args:
            attrs: Атрибуты для передачи в представление

        Returns:
            attrs: Неизмененные атрибуты

        """
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации и профиля пользователя."""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "middle_name",
            "password",
        ]

    def create(self, validated_data):
        """Создает пользователя с ролью 'User'.

        Args:
            validated_data: Данные пользователя

        Returns:
            User: Созданный пользователь
        """
        password = validated_data.pop("password")
        user_role, _ = Role.objects.get_or_create(name="User")
        user = User.objects.create_user(
            role=user_role,
            password=password,
            **validated_data
        )
        return user


class RoleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Role."""

    class Meta:
        model = Role
        fields = ["id", "name"]


class BusinessElementSerializer(serializers.ModelSerializer):
    """Сериализатор для модели BusinessElement."""

    class Meta:
        model = BusinessElement
        fields = ["id", "name"]


class AccessRuleSerializer(serializers.ModelSerializer):
    """Сериализатор для управления правилами доступа."""

    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), source="role"
    )
    element_id = serializers.PrimaryKeyRelatedField(
        queryset=BusinessElement.objects.all(), source="element"
    )

    class Meta:
        model = AccessRule
        fields = [
            "id",
            "role_id",
            "element_id",
            "read_permission",
            "read_all_permission",
            "create_permission",
            "update_permission",
            "update_all_permission",
            "delete_permission",
            "delete_all_permission",
        ]

