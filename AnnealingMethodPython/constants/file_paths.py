import sys
from pathlib import Path

def get_base_path() -> Path:
    """
    Возвращает путь к директории с EXE (или к проекту в dev-режиме).

    Returns:
        Path: Абсолютный путь к папке с exe или к корню проекта.
    """
    if getattr(sys, "frozen", False):
        # Для скомпилированного EXE берём директорию исполняемого файла
        return Path(sys.argv[0]).parent
    else:
        # Для разработки возвращаем корень проекта
        return Path(__file__).parent.parent

# Путь к hamiltonian_operators.txt (внешний файл)
HAMILTONIAN_FILE_PATH: Path = get_base_path() / "params" / "hamiltonian_operators.txt"

# Файл вывода создаётся в текущей рабочей директории
OUTPUT_FILE_PATH: Path = get_base_path() / "output.log"
