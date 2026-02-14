"""Представления бизнес-логики проекта."""

from rest_framework.views import APIView
from rest_framework.response import Response
from custom_auth.permissions import AccessPermission
from rest_framework.permissions import IsAuthenticated


class ProductListView(APIView):
    """Список доступных продуктов."""
    permission_classes = [IsAuthenticated, AccessPermission]
    required_permission = 'read'
    element_id = 2  # id BusinessElement для «products» (согласовано с фикстурами)

    def get(self, request):
        """Возвращает список продуктов."""
        return Response({'products': ['Product A', 'Product B']})


class OrderListView(APIView):
    """Список заказов пользователя."""
    permission_classes = [IsAuthenticated, AccessPermission]
    required_permission = 'read'
    element_id = 3  # id BusinessElement для «orders» (согласовано с фикстурами)

    def get(self, request):
        """Возвращает список заказов."""
        return Response({'orders': ['Order X', 'Order Y']})


class UserListView(APIView):
    """Список пользователей системы."""
    permission_classes = [IsAuthenticated, AccessPermission]
    required_permission = 'read'
    element_id = 1  # id BusinessElement для «users» (согласовано с фикстурами)

    def get(self, request):
        """Возвращает список пользователей."""
        return Response({'users': ['User1', 'User2']})
