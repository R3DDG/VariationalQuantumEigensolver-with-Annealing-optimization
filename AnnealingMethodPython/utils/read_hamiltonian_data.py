import numpy as np
from typing import List, Tuple
from .read_file_lines import read_file_lines

def read_hamiltonian_data(file_path) -> Tuple[List[Tuple[complex, List[int]]], List[List[int]]]:
    """
    Читает данные из файла hamiltonian_operators.txt и возвращает два списка:
    - Список операторов Паули в виде коэффициента оператора и строки Паули.
    - Список строк операторов Паули.

    Args:
        file_path (str | Path): Путь к файлу.

    Returns:
        Tuple[List[Tuple[complex, List[int]]], List[List[int]]]: (pauli_operators, pauli_strings)

    Raises:
        FileNotFoundError: Если файл не найден.
    """
    lines = read_file_lines(file_path, ignore_comments=False)
    pauli_operators: List[Tuple[complex, List[int]]] = []
    pauli_strings: List[List[int]] = []
    for line in lines:
        # Разделение строки на компоненты
        parts = line.strip().split()
        if len(parts) == 3:
            real_part, imag_part, index_str = (
                float(parts[0]),
                float(parts[1]),
                str(parts[2]),
            )
            coefficient = np.complex128(real_part + imag_part * 1j)
            index_list = [int(c) for c in index_str]
            if coefficient != 0:  # Игнорирование нулевых коэффициентов
                pauli_operators.append((coefficient, index_list))
            pauli_strings.append(index_list)
    return pauli_operators, pauli_strings
