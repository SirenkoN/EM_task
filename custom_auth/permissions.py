from rest_framework import permissions

class AccessPermission(permissions.BasePermission):
    """
    Проверяет, имеет ли авторизованный пользователь нужные права на конкретный ресурс.
    View должен установить:
        required_permission = 'read' | 'create' | ...  # действие
        element_id = <id>  # id бизнес‑элемента
    """

    def has_permission(self, request, view):
        # Если не авторизован – DRF вернёт 401 автоматически
        if not request.user or not request.user.is_active:
            return False

        required = getattr(view, 'required_permission', None)
        element_id = getattr(view, 'element_id', None)

        # Без указания прав – считаем доступным (используем для демонстрации)
        if not required or not element_id:
            return True

        from auth.models import AccessRule
        try:
            rule = AccessRule.objects.get(
                role=request.user.role,
                element_id=element_id
            )
        except AccessRule.DoesNotExist:
            return False  # пользователь не имеет прав

        # Проверяем конкретное поле
        if required == 'read':
            return rule.read_permission or rule.read_all_permission
        elif required == 'create':
            return rule.create_permission
        elif required == 'update':
            return rule.update_permission or rule.update_all_permission
        elif required == 'delete':
            return rule.delete_permission or rule.delete_all_permission

        return False  # неизвестное действие -> отказ
