from rich.table import Table
from rich.panel import Panel
from rich import box
from typing import List, Dict, Any

def create_table(
    columns: List[Dict[str, str]],
    data: List[List[Any]],
    title: str,
    border_style: str = "yellow",
) -> Panel:
    """
    Создает таблицу rich.Table и оборачивает ее в rich.Panel для консольного вывода.

    Args:
        columns (List[Dict[str, str]]): Описание столбцов (ключи: name, style, justify).
        data (List[List[Any]]): Массив данных для строк таблицы.
        title (str): Заголовок панели.
        border_style (str): Цвет рамки панели.

    Returns:
        Panel: Панель с таблицей для печати в консоль.
    """
    table = Table(box=box.ROUNDED, border_style=border_style)
    for col in columns:
        table.add_column(
            col["name"],
            justify=col.get("justify", "default"),
            style=col.get("style", ""),
        )
    for row in data:
        table.add_row(*row)
    return Panel(table, title=title, border_style=border_style)
