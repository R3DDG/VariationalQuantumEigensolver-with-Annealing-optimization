from rich.console import Console
from typing import Any
from constants.file_paths import OUTPUT_FILE_PATH

def console_and_print(console: Console, message: Any) -> None:
    """
    Выводит сообщение в консоль и дублирует его в лог-файл.

    Args:
        console (Console): объект rich.Console для форматированного вывода.
        message (Any): строка, rich.Panel или другой объект, печатаемый в консоль.

    Примечания:
        - Используется rich для красивого форматирования в консоли и логах.
        - Лог хранит весь вывод, включая цветовые коды (если export_text это поддерживает).
    """
    console.print(message)
    with open(OUTPUT_FILE_PATH, "a", encoding="utf-8") as file:
        file.write(console.export_text() + "\n")
