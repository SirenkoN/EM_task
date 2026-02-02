from rest_framework.views import APIView
from rest_framework.response import Response
from custom_auth.permissions import AccessPermission

# ------------------- Список продуктов ---------------------------------

class ProductListView(APIView):
    required_permission = 'read'
    element_id = 1  # id BusinessElement для «products»

    def get(self, request):
        if not AccessPermission().has_permission(request, self):
            return Response(status=403)  # Forbidden
        return Response({'products': ['Product A', 'Product B']})

# ------------------- Список заказов ---------------------------------

class OrderListView(APIView):
    required_permission = 'read'
    element_id = 2  # id BusinessElement для «orders»

    def get(self, request):
        if not AccessPermission().has_permission(request, self):
            return Response(status=403)
        return Response({'orders': ['Order X', 'Order Y']})

# ------------------- Список пользователей ---------------------------------

class UserListView(APIView):
    required_permission = 'read'
    element_id = 3  # id BusinessElement для «users»

    def get(self, request):
        if not AccessPermission().has_permission(request, self):
            return Response(status=403)
        return Response({'users': ['User1', 'User2']})
