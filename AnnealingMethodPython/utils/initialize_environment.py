from rich.console import Console
from constants.file_paths import OUTPUT_FILE_PATH

def initialize_environment() -> Console:
    """
    Инициализирует окружение, очищает файл вывода и возвращает объект rich.Console.

    Returns:
        Console: Объект rich.Console.
    """
    if OUTPUT_FILE_PATH.exists():
        OUTPUT_FILE_PATH.unlink()
    return Console(force_terminal=True, color_system="truecolor", record=True)
