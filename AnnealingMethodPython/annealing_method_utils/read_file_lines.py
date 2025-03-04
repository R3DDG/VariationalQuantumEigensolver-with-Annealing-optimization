from pathlib import Path

def read_file_lines(file_path: str | Path, ignore_comments: bool = True) -> list[str]:
    """
    Читает строки из файла, игнорируя комментарии (строки, начинающиеся с '#').

    :param file_path: Путь к файлу.
    :param ignore_comments: Игнорировать строки, начинающиеся с '#'.
    :return: Список строк.
    :raises FileNotFoundError: Если файл не найден.
    """
    file_path = Path(file_path) if not isinstance(file_path, Path) else file_path
    if not file_path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if not (ignore_comments and line.strip().startswith('#'))]