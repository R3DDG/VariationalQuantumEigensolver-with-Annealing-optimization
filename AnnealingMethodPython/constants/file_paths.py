import sys
from pathlib import Path

def get_base_path() -> Path:
    """
    Определяет базовую директорию проекта.

    Returns:
        Path: Абсолютный путь к папке с .exe-файлом (если приложение заморожено)
              или к корню проекта (в режиме разработки).

    Примечания:
        - sys.frozen (атрибут пакета PyInstaller) используется для определения,
          был ли код скомпилирован в исполняемый файл.
        - Это позволяет корректно определять относительные пути при запуске
          как из исходников, так и из собранного .exe.
    """
    if getattr(sys, "frozen", False):
        # Для скомпилированного EXE возвращаем директорию исполняемого файла.
        return Path(sys.argv[0]).parent
    else:
        # Для разработки возвращаем корень проекта (на уровень выше constants/).
        return Path(__file__).parent.parent

# Абсолютный путь к файлу с гамильтонианом (описание операторов Паули и их коэффициентов).
HAMILTONIAN_FILE_PATH: Path = get_base_path() / "params" / "hamiltonian_operators.txt"

# Абсолютный путь к файлу для логирования вывода (очищается при запуске).
OUTPUT_FILE_PATH: Path = get_base_path() / "output.log"
