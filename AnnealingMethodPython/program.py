import numpy as np  # Для работы с комплексными числами и математическими операциями
import random  # Для генерации случайных чисел
import sys  # Для работы с системными параметрами и настройки стандартного ввода/вывода
import io  # Для работы с потоками ввода/вывода и настройки кодировки
from rich.panel import Panel  # Для панелей с текстом
from typing import Tuple, List, Dict

# Импорт самописных util функций
from utils.console_and_print import console_and_print
from utils.print_pauli_table import print_pauli_table
from utils.read_hamiltonian_data import read_hamiltonian_data
from utils.print_hamiltonian import print_hamiltonian
from utils.format_ansatz import format_ansatz
from utils.initialize_environment import initialize_environment
from utils.print_theta_table import print_theta_table
from utils.print_composition_table import print_composition_table

# Импорт констант
from constants.file_paths import HAMILTONIAN_FILE_PATH
from constants.pauli import PAULI_MAP

# Устанавливаем кодировку для стандартного вывода
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


def generate_random_theta(m: int) -> np.ndarray:
    """Генерирует массив из m случайных чисел в диапазоне [0, 1)."""
    return np.random.rand(m).astype(np.float64)


def multiply_pauli(i: int, j: int) -> Tuple[complex, int]:
    """
    Вычисляет произведение базисных операторов Паули.

    Возвращает:
        Tuple[complex, int]: (коэффициент, индекс результата)
    """
    if i == j:
        return (1, 0)
    if i == 0:
        return (1, j)
    if j == 0:
        return (1, i)
    return PAULI_MAP.get((i, j), (1, 0))


def pauli_compose(s1: List[int], s2: List[int]) -> Tuple[complex, List[int]]:
    """
    Вычисляет композицию двух операторов Паули.

    Возвращает:
        Tuple[complex, List[int]]: (коэффициент, результирующий оператор)
    """
    coefficient = 1.0
    result = []
    for a, b in zip(s1, s2):
        coeff, idx = multiply_pauli(a, b)
        coefficient *= coeff
        result.append(idx)
    return coefficient, result


def calculate_ansatz(
    theta: np.ndarray, pauli_operators: List[Tuple[complex, List[int]]]
) -> Tuple[str, str]:
    """
    Вычисляет анзац как произведение экспонент операторов Паули.

    Возвращает:
        Tuple[str, str]: (символьное представление, численное представление)
    """
    operator_length = len(pauli_operators[0][1])
    result = {tuple([0] * operator_length): 1.0}

    for t, (coeff, op) in zip(theta, pauli_operators):
        cos_t = np.cos(t)
        sin_t = np.sin(t)

        new_result: Dict[Tuple[int, ...], complex] = {}

        for existing_op, existing_coeff in result.items():
            # Обработка единичного оператора (cos(t)*I)
            identity_coeff = existing_coeff * cos_t
            new_op = tuple(existing_op)
            new_result[new_op] = new_result.get(new_op, 0) + identity_coeff

            # Обработка оператора Паули (1j*sin(t)*sigma)
            pauli_coeff = existing_coeff * 1j * sin_t * coeff
            compose_coeff, compose_op = pauli_compose(list(existing_op), op)
            final_coeff = pauli_coeff * compose_coeff
            final_op = tuple(compose_op)
            new_result[final_op] = new_result.get(final_op, 0) + final_coeff

        result = new_result

    return format_ansatz(pauli_operators, result)


def main():
    """Основная логика программы."""
    console = initialize_environment()

    try:
        pauli_operators, pauli_strings = read_hamiltonian_data(HAMILTONIAN_FILE_PATH)
    except FileNotFoundError:
        console_and_print(console, f"[red]Файл {HAMILTONIAN_FILE_PATH} не найден[/red]")
        return

    if not pauli_operators:
        console_and_print(console, "[red]Нет операторов Паули для обработки[/red]")
        return

    print_hamiltonian(console, pauli_operators)
    print_pauli_table(console, pauli_operators)
    print_composition_table(console, pauli_compose, pauli_strings)

    m = random.randint(1, len(pauli_operators) - 1)
    theta = generate_random_theta(m)
    print_theta_table(console, theta)

    ansatz_symbolic, ansatz_numeric = calculate_ansatz(theta, pauli_operators[:m])

    console_and_print(
        console, Panel(ansatz_symbolic, title="[bold]U(θ)[/bold]", border_style="green")
    )
    console_and_print(
        console, Panel(ansatz_numeric, title="[bold]U[/bold]", border_style="purple")
    )


if __name__ == "__main__":
    main()
