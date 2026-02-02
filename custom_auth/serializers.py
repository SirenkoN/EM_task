from rest_framework import serializers
from .models import User, Role, BusinessElement, AccessRule

# --------------------------------------------------------------------
# Сериализатор для пользователя (регистрация и профиль)
# --------------------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # пароль вводится только один раз в API

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'middle_name']

    def create(self, validated_data):
        """Создаём пользователя и хешируем пароль."""
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


# --------------------------------------------------------------------
# Сериализаторы для ролей и бизнес‑элементов
# --------------------------------------------------------------------
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']


class BusinessElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessElement
        fields = ['id', 'name']


# --------------------------------------------------------------------
# Сериализатор для правил доступа
# --------------------------------------------------------------------
class AccessRuleSerializer(serializers.ModelSerializer):
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), source='role')
    element_id = serializers.PrimaryKeyRelatedField(
        queryset=BusinessElement.objects.all(), source='element')

    class Meta:
        model = AccessRule
        fields = [
            'id', 'role_id', 'element_id',
            'read_permission', 'read_all_permission',
            'create_permission', 'update_permission',
            'update_all_permission', 'delete_permission',
            'delete_all_permission'
        ]
