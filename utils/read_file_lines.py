from pathlib import Path
from typing import List, Union

def read_file_lines(file_path: Union[str, Path], ignore_comments: bool) -> List[str]:
    file_path = Path(file_path) if not isinstance(file_path, Path) else file_path
    if not file_path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    with open(file_path, "r") as file:
        return [
            line.strip()
            for line in file
            if not (ignore_comments and line.strip().startswith("#"))
        ]
