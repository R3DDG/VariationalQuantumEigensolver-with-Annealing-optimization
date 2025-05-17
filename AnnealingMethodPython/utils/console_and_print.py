from rich.console import Console
from typing import Any
from constants.file_paths import OUTPUT_FILE_PATH

def console_and_print(console: Console, message: Any) -> None:
    """
    Выводит результат выполнения программы в файл и консоль.

    Args:
        console (Console): Объект rich.Console для консольного вывода.
        message (Any): Сообщение для вывода (строка, панель и т.д.).
    """
    console.print(message)
    # Экспортируем всё содержимое консоли (в т.ч. цвета) в файл
    with open(OUTPUT_FILE_PATH, "a", encoding="utf-8") as file:
        file.write(console.export_text() + "\n")
