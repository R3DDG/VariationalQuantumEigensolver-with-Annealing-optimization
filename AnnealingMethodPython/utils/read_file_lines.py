from pathlib import Path
from typing import List, Union

def read_file_lines(file_path: Union[str, Path], ignore_comments: bool) -> List[str]:
    """
    Считывает строки из файла, игнорируя комментарии (начинающиеся с "#").

    Args:
        file_path (str|Path): Путь к файлу.
        ignore_comments (bool): Если True, строки, начинающиеся с "#", игнорируются.

    Returns:
        List[str]: Список строк без лишних пробелов и пустых строк.

    Raises:
        FileNotFoundError: Если файл не существует.
    """
    file_path = Path(file_path) if not isinstance(file_path, Path) else file_path
    if not file_path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    with open(file_path, "r") as file:
        return [
            line.strip()
            for line in file
            if not (ignore_comments and line.strip().startswith("#"))
        ]
