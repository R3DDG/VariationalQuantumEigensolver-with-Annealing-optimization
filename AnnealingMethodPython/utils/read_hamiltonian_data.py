import numpy as np
from typing import List, Tuple
from .read_file_lines import read_file_lines

def read_hamiltonian_data(file_path) -> Tuple[List[Tuple[complex, List[int]]], List[List[int]]]:
    """
    Читает список операторов Паули из текстового файла.

    Формат файла:
        <действительная часть> <мнимая часть> <строка Паули>

    Returns:
        Tuple[List[Tuple[complex, List[int]]], List[List[int]]]:
            - Список операторов (коэффициент, индексы Паули)
            - Список только индексов (без коэффициентов)
    """
    lines = read_file_lines(file_path, ignore_comments=False)
    pauli_operators: List[Tuple[complex, List[int]]] = []
    pauli_strings: List[List[int]] = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) == 3:
            real_part, imag_part, index_str = (
                float(parts[0]),
                float(parts[1]),
                str(parts[2]),
            )
            coefficient = np.complex128(real_part + imag_part * 1j)
            index_list = [int(c) for c in index_str]
            if coefficient != 0:
                pauli_operators.append((coefficient, index_list))
            pauli_strings.append(index_list)
    return pauli_operators, pauli_strings
