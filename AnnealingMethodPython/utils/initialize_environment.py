from rich.console import Console
from constants.file_paths import OUTPUT_FILE_PATH

def initialize_environment() -> Console:
    """
    Инициализирует окружение для запуска программы:
    - Очищает лог-файл с прошлых запусков.
    - Возвращает объект rich.Console для форматированного вывода.

    Returns:
        Console: Готовый к использованию rich.Console.
    """
    if OUTPUT_FILE_PATH.exists():
        OUTPUT_FILE_PATH.unlink()
    return Console(force_terminal=True, color_system="truecolor", record=True)
