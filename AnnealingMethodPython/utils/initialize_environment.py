from rich.console import Console  # Для красивого вывода в консоль
from constants.file_paths import OUTPUT_FILE_PATH


def initialize_environment() -> Console:
    """Инициализирует окружение и возвращает консольный объект."""
    if OUTPUT_FILE_PATH.exists():
        OUTPUT_FILE_PATH.unlink()
    return Console(force_terminal=True, color_system="truecolor", record=True)
