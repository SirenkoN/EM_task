from rest_framework import permissions

class AccessPermission(permissions.BasePermission):
    """
    Проверяет, имеет ли авторизованный пользователь нужные права на конкретный ресурс.
    View должен установить:
        required_permission = 'read' | 'create' | ...  # действие
        element_id = <id>  # id бизнес‑элемента
    """

    def has_permission(self, request, view):
        """Проверяет разрешение пользователя на выполнение действия над бизнес-элементом.

        Выполняет последовательную проверку:
        1. Активен ли пользователь
        2. Указаны ли required_permission и element_id в представлении
        3. Является ли пользователь администратором (автоматически получает все права)
        4. Наличие роли у пользователя
        5. Проверка конкретного правила доступа из БД в зависимости от required_permission

        Args:
            request: HTTP-запрос с аутентификационными данными
            view: Представление, для которого проверяется доступ

        Returns:
            bool: True если доступ разрешен, False в противном случае

        Побочные эффекты:
            - Для администраторов всегда возвращает True
            - При отсутствии element_id или required_permission возвращает True
            - Для неактивных пользователей всегда возвращает False
        """
        if not request.user or not request.user.is_active:
            return False

        required = getattr(view, 'required_permission', None)
        element_id = getattr(view, 'element_id', None)

        # Без указания прав – считаем доступным (используем для демонстрации)
        if not required or not element_id:
            return True

        # Проверка для администратора - имеет все права
        if request.user.role and hasattr(request.user.role, 'name') and request.user.role.name == "Admin":
            return True

        # Проверяем, есть ли у пользователя роль
        if not request.user.role:
            return False

        from custom_auth.models import AccessRule
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


