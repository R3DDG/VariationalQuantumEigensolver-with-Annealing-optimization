from rich.table import Table  # Для создания таблиц
from rich.panel import Panel  # Для панелей с текстом
from rich import box  # Для стилизации таблиц


def create_table(columns, data, title, border_style="yellow"):
    """
    Создает таблицу с заданными колонками и данными.

    :param columns: Список словарей с описанием колонок.
    :param data: Данные для таблицы.
    :param title: Заголовок таблицы.
    :param border_style: Стиль границы таблицы.
    :return: Панель с таблицей.
    """
    table = Table(box=box.ROUNDED, border_style="yellow")
    for col in columns:
        table.add_column(
            col["name"],
            justify=col.get("justify", "default"),
            style=col.get("style", ""),
        )
    for row in data:
        table.add_row(*row)
    return Panel(table, title=title, border_style=border_style)
