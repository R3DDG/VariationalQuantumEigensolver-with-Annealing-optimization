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
) -> Tuple[Dict[Tuple[int, ...], complex], str, str]:
    """
    Вычисляет анзац в виде произведения экспонент операторов Паули.

    Args:
        theta (np.ndarray): Массив параметров [θ₁, θ₂, ..., θₘ]
        pauli_operators (List[Tuple[complex, List[int]]]): Список операторов вида (коэффициент, [индексы Паули])

    Returns:
        Tuple:
            - Словарь {оператор: коэффициент}
            - Символьное представление анзаца
            - Численное представление анзаца
    """
    # Каждый оператор Паули представляется как exp(iθ(coefficient * σ))
    # Раскладываем экспоненту по формуле Эйлера:
    # e^{iθσ} = cos(θ)I + i sin(θ)σ
    # Инициализация единичным оператором
    operator_length = len(pauli_operators[0][1])
    result = {tuple([0] * operator_length): 1.0}

    # Последовательно применяем каждый оператор из списка
    for t, (coeff, op) in zip(theta, pauli_operators):
        cos_t = np.cos(t)
        sin_t = np.sin(t)

        new_result: Dict[Tuple[int, ...], complex] = {}

        # Обработка всех существующих операторов в анзаце
        for existing_op, existing_coeff in result.items():
            # Слагаемое с cos(θ)*I
            identity_coeff = existing_coeff * cos_t
            new_result[existing_op] = new_result.get(existing_op, 0) + identity_coeff

            # Слагаемое с i*sin(θ)*σ
            pauli_coeff = existing_coeff * 1j * sin_t * coeff
            compose_coeff, compose_op = pauli_compose(list(existing_op), op)
            final_coeff = pauli_coeff * compose_coeff
            final_op = tuple(compose_op)
            new_result[final_op] = new_result.get(final_op, 0) + final_coeff

        result = new_result
        symbolic_str, numeric_str = format_ansatz(pauli_operators, result)
    return result, symbolic_str, numeric_str


def compute_uhu(
    u_dict: Dict[Tuple[int, ...], complex], h_terms: List[Tuple[complex, List[int]]]
) -> Dict[Tuple[int, ...], complex]:
    """
    Вычисляет оператор U† H U.

    Args:
        u_dict (Dict): Анзац U в виде {оператор: коэффициент}
        h_terms (List): Гамильтониан H как список термов (коэффициент, оператор)

    Returns:
        Dict: Результат U†HU в виде {оператор: коэффициент}
    """
    # Алгоритм вычисления U†HU:
    # 1. Для каждого терма H: coeff_h * op_h
    # 2. Умножаем слева на U† (сопряжение коэффициентов)
    # 3. Умножаем справа на U
    # 4. Суммируем все вклады
    uhu_dict: Dict[Tuple[int, ...], complex] = {}

    # Проходим по всем термам гамильтониана
    for coeff_h, op_h in h_terms:
        # U† H часть
        for j_op, j_coeff in u_dict.items():
            conjugated_j_coeff = np.conj(j_coeff)  # Сопряжение для U†
            c1, op_uh = pauli_compose(list(j_op), op_h)

            # (U† H) U часть
            for k_op, k_coeff in u_dict.items():
                c2, op_uhu = pauli_compose(op_uh, list(k_op))
                total_coeff = conjugated_j_coeff * k_coeff * coeff_h * c1 * c2
                op_tuple = tuple(op_uhu)
                uhu_dict[op_tuple] = uhu_dict.get(op_tuple, 0) + total_coeff

    return uhu_dict


def calculate_expectation(uhu_dict: Dict[Tuple[int, ...], complex]) -> float:
    """
    Вычисляет ⟨0|U†HU|0⟩ для состояния |0...0⟩.

    Args:
        uhu_dict (Dict): Результат U†HU от compute_uhu

    Returns:
        float: Ожидаемое значение
    """
    # Состояние |0...0⟩ коллапсирует все недиагональные операторы
    # к нулю, поэтому учитываем только диагональные компоненты (I и Z)
    expectation = 0.0
    for op, coeff in uhu_dict.items():
        # Фильтрация операторов с только I (0) и Z (3)
        if all(p in {0, 3} for p in op):
            expectation += coeff.real  # Мнимая часть автоматически обнуляется
    return expectation


def test_pauli_multipliation():
    """Тесты для проверки умножения операторов Паули"""
    coeff, idx = multiply_pauli(1, 2)
    assert np.isclose(coeff, 1j) and idx == 3, "Ошибка в умножении X*Y"

    coeff, op = pauli_compose([1], [2])
    assert np.isclose(coeff, 1j) and op == [3], "Ошибка в композиции X*Y"


def main():
    """Основная логика программы."""
    console = initialize_environment()
    test_pauli_multipliation()

    try:
        pauli_operators, pauli_strings = read_hamiltonian_data(HAMILTONIAN_FILE_PATH)
    except FileNotFoundError:
        console_and_print(console, f"[red]Файл {HAMILTONIAN_FILE_PATH} не найден[/red]")
        return

    if not pauli_operators:
        console_and_print(console, "[red]Нет операторов Паули для обработки[/red]")
        return

    if len(pauli_operators) < 2:
        console_and_print(console, "[red]Нужно минимум 2 оператора Паули[/red]")
        return

    print_hamiltonian(console, pauli_operators)
    print_pauli_table(console, pauli_operators)
    print_composition_table(console, pauli_compose, pauli_strings)

    m = random.randint(1, len(pauli_operators) - 1)  # m строго < len(operators)
    theta = generate_random_theta(m)
    print_theta_table(console, theta)

    ansatz_dict, ansatz_symbolic, ansatz_numeric = calculate_ansatz(
        theta, pauli_operators[:m]
    )

    console_and_print(
        console, Panel(ansatz_symbolic, title="[bold]U(θ)[/bold]", border_style="green")
    )
    console_and_print(
        console, Panel(ansatz_numeric, title="[bold]U[/bold]", border_style="purple")
    )

    # Вычисление ⟨U|H|U⟩
    uhu_dict = compute_uhu(ansatz_dict, pauli_operators)
    expectation = calculate_expectation(uhu_dict)
    console_and_print(
        console,
        Panel(f"⟨U|H|U⟩ = {expectation:.4f}", title="⟨U|H|U⟩", border_style="green"),
    )


if __name__ == "__main__":
    main()
