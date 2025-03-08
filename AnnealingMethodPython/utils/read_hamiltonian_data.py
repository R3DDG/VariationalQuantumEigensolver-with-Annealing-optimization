import numpy as np  # Для работы с комплексными числами и математическими операциями
from .read_file_lines import read_file_lines


def read_hamiltonian_data(file_path):
    """
    Читает данные из файла hamiltonian_operators.txt и возвращает два списка:
    - Список операторов Паули в виде коэффициента оператора и строки Паули.
    - Список строк операторов Паули.

    :param file_path: Путь к файлу.
    :return: (pauli_operators, pauli_strings)
    :raises FileNotFoundError: Если файл не найден.
    """
    lines = read_file_lines(file_path, ignore_comments=False)
    pauli_operators = []
    pauli_strings = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) == 3:
            real_part, imag_part, index = (
                float(parts[0]),
                float(parts[1]),
                str(parts[2]),
            )
            coefficient = np.complex128(real_part + imag_part * 1j)
            if coefficient != 0:
                pauli_operators.append((coefficient, index))
            pauli_strings.append([int(c) for c in parts[2]])
    return pauli_operators, pauli_strings
