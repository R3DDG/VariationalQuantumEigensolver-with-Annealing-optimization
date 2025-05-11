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
        # Разделение строки на компоненты
        parts = line.strip().split()
        if len(parts) == 3:
            real_part, imag_part, index_str = (
                float(parts[0]),
                float(parts[1]),
                str(parts[2]),
            )
            # Преобразование в комплексное число
            coefficient = np.complex128(real_part + imag_part * 1j)
            # Парсинг строки Паули
            index_list = [int(c) for c in index_str]  
            if coefficient != 0: # Игнорирование нулевых коэффициентов
                pauli_operators.append((coefficient, index_list))
            pauli_strings.append(index_list)
    return pauli_operators, pauli_strings
