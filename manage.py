#!/usr/bin/env python
import os
import sys

def main():
    # Устанавливаем переменную окружения, указывающую на файл settings.py
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. "
            "Убедитесь, что он установлен и доступен в PYTHONPATH."
        ) from exc
    # Выполняем команду из аргументов командной строки
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
