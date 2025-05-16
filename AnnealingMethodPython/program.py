import numpy as np
import sys
import io
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from rich.panel import Panel
from functools import lru_cache
from typing import Tuple, List, Dict

# Импорт самописных util функций
from utils.console_and_print import console_and_print
from utils.print_pauli_table import print_pauli_table
from utils.read_hamiltonian_data import read_hamiltonian_data
from utils.print_hamiltonian import print_hamiltonian
from utils.print_composition_table import print_composition_table
from utils.format_ansatz import format_ansatz
from utils.initialize_environment import initialize_environment
from utils.calculate_temp_steps import calculate_temp_steps

# Импорт констант
from constants.file_paths import HAMILTONIAN_FILE_PATH
from constants.pauli import PAULI_MAP

# Установка кодировки для корректного вывода
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


def generate_shifted_theta(pauli_operators: List[Tuple[complex, List[int]]]) -> np.ndarray:
    """Генерирует θ на основе коэффициентов операторов (вектор сдвига)."""
    if not pauli_operators:
        return np.array([], dtype=np.float64)
    
    # Извлечение модулей действительных частей
    coeffs = np.array([abs(op[0].real) for op in pauli_operators], dtype=np.float64)
    norm = np.linalg.norm(coeffs)
    if norm < 1e-12:
        return np.zeros(len(coeffs))
    
    # Масштабируем в [0, 2π) и добавляем шум
    scaled = (coeffs / norm) * 2 * np.pi
    return scaled + np.random.normal(0, 0.1, len(scaled))


def multiply_pauli(i: int, j: int) -> Tuple[complex, int]:
    """
    Вычисляет произведение базисных операторов Паули.
    Возвращает: (коэффициент, индекс результата)
    """
    if i == j:
        return (1, 0)
    if i == 0:
        return (1, j)
    if j == 0:
        return (1, i)
    return PAULI_MAP.get((i, j), (1, 0))


@lru_cache(maxsize=4096)
def pauli_compose(s1: List[int], s2: List[int]) -> Tuple[complex, Tuple[int, ...]]:
    """
    Вычисляет композицию двух операторов Паули.
    Возвращает: (коэффициент, результирующий оператор)
    """
    s1_tuple = tuple(s1)
    s2_tuple = tuple(s2)
    coefficient = 1.0
    result = []
    for a, b in zip(s1_tuple, s2_tuple):
        coeff, idx = multiply_pauli(a, b)
        coefficient *= coeff
        result.append(idx)
    return coefficient, tuple(result)


def calculate_ansatz(
    theta: np.ndarray, pauli_operators: List[Tuple[complex, List[int]]]
) -> Dict[Tuple[int, ...], complex]:
    """
    Вычисляет анзац в виде произведения экспонент операторов Паули.
    Возвращает: (словарь операторов, символьное представление, численное представление)
    """
    operator_length = len(pauli_operators[0][1])
    result = {tuple([0]*operator_length): 1.0}

    for t, (_, op) in zip(theta, pauli_operators):
        cos_t = np.cos(t)
        sin_t = np.sin(t)
        new_result = {}
        op_tuple = tuple(op)
        for existing_op, existing_coeff in result.items():
            # cos(θ) * I
            new_result[existing_op] = new_result.get(existing_op, 0) + existing_coeff * cos_t
            # i*sin(θ)*σ
            compose_coeff, compose_op = pauli_compose(tuple(existing_op), tuple(op_tuple))
            final_coeff = existing_coeff * 1j * sin_t * compose_coeff
            new_result[compose_op] = new_result.get(compose_op, 0) + final_coeff
        result = new_result
        
    symbolic_str, numeric_str = format_ansatz(pauli_operators, result)
    return result, symbolic_str, numeric_str


def compute_uhu(
    u_dict: Dict[Tuple[int, ...], complex], h_terms: List[Tuple[complex, List[int]]]
) -> Dict[Tuple[int, ...], complex]:
    """
    Вычисляет оператор U† H U.
    Возвращает: словарь {оператор: коэффициент}
    """
    uhu_dict = {}
    u_items = list(u_dict.items())
    for coeff_h, op_h in h_terms:
        op_h_tuple = tuple(op_h)
        for j_op, j_coeff in u_items:
            conj_j_coeff = np.conj(j_coeff)
            c1, op_uh = pauli_compose(j_op, op_h_tuple)
            for k_op, k_coeff in u_items:
                c2, op_uhu = pauli_compose(op_uh, k_op)
                total_coeff = conj_j_coeff * k_coeff * coeff_h * c1 * c2
                uhu_dict[op_uhu] = uhu_dict.get(op_uhu, 0) + total_coeff
    return uhu_dict


def calculate_expectation(uhu_dict: Dict[Tuple[int, ...], complex]) -> float:
    """
    Вычисляет ⟨0|U†HU|0⟩ для состояния |0...0⟩.
    Возвращает: ожидаемое значение
    """
    expectation = 0.0
    for op, coeff in uhu_dict.items():
        if all(p in (0, 3) for p in op):  # I или Z
            expectation += coeff.real
    return expectation


def generate_neighbor_theta(
    current_theta: np.ndarray, step_size: float = 0.1
) -> np.ndarray:
    """Генерирует соседнее решение, добавляя случайное изменение к текущему theta."""
    perturbation = np.random.normal(scale=step_size, size=current_theta.shape)
    return np.clip(current_theta + perturbation, 0.0, 1.0)


def simulated_annealing(
    initial_theta: np.ndarray,
    pauli_operators: list,
    progress,
    task,
    initial_temp: float = 1000.0,
    cooling_rate: float = 0.99,
    min_temp: float = 1e-5,
    num_iterations_per_temp: int = 500,
    step_size: float = 0.5,
) -> tuple:
    """Алгоритм отжига с термализацией."""
    current_theta = initial_theta.copy()
    best_theta = current_theta.copy()
    best_energy = float("inf")
    rng = np.random.default_rng()
    temp = initial_temp
    thermalization_steps = int(num_iterations_per_temp * 0.2)

    while temp > min_temp:
        # Термализация (можно уменьшить число шагов)
        for _ in range(thermalization_steps):
            current_theta = generate_shifted_theta(pauli_operators)
            ansatz_dict, _, _ = calculate_ansatz(current_theta, pauli_operators)
            uhu_dict = compute_uhu(ansatz_dict, pauli_operators)
            current_energy = calculate_expectation(uhu_dict)
            if current_energy < best_energy:
                best_theta = current_theta.copy()
                best_energy = current_energy
            if progress is not None:
                progress.update(task, advance=1)

        # Основной цикл отжига
        for _ in range(num_iterations_per_temp):
            perturbation = rng.normal(0, step_size*(temp/initial_temp), current_theta.shape)
            neighbor_theta = (current_theta + perturbation) % (2*np.pi)
            ansatz_dict, _, _ = calculate_ansatz(neighbor_theta, pauli_operators)
            uhu_dict = compute_uhu(ansatz_dict, pauli_operators)
            current_energy = calculate_expectation(uhu_dict)
            energy_diff = current_energy - best_energy
            if energy_diff < 0 or rng.random() < np.exp(-energy_diff / temp):
                current_theta = neighbor_theta.copy()
                if current_energy < best_energy:
                    best_theta = current_theta.copy()
                    best_energy = current_energy
            if progress is not None:
                progress.update(task, advance=1)
        temp *= cooling_rate

    return best_theta, best_energy


def main():
    """Основная логика программы."""
    console = initialize_environment()

    if not HAMILTONIAN_FILE_PATH.exists():
        msg = (
            f"Файл [bold]{HAMILTONIAN_FILE_PATH}[/] не найден!\n"
            "Убедитесь, что рядом с EXE есть папка [bold]params[/] с файлом [bold]hamiltonian_operators.txt[/]."
        )
        console_and_print(console, Panel(msg, border_style="red"))
        return

    try:
        pauli_operators, pauli_strings = read_hamiltonian_data(HAMILTONIAN_FILE_PATH)
        print_hamiltonian(console, pauli_operators)
        print_pauli_table(console, pauli_operators)
        print_composition_table(console, pauli_compose, pauli_strings)
    except FileNotFoundError:
        console_and_print(console, Panel(f"[red]Файл {HAMILTONIAN_FILE_PATH} не найден[/red]", border_style="red"))
        return

    if len(pauli_operators) < 2:
        console_and_print(console, Panel("[red]Требуется минимум 2 оператора Паули[/red]", border_style="red"))
        return

    # Параметры алгоритма отжига
    SA_PARAMS = {
        "initial_temp": 100.0,
        "cooling_rate": 0.95,
        "min_temp": 1e-3,
        "num_iterations_per_temp": 100,
        "step_size": 0.1,
    }

    # Рассчитываем общее количество шагов
    thermalization_steps = int(SA_PARAMS["num_iterations_per_temp"] * 0.2)
    temp_steps = calculate_temp_steps(
        SA_PARAMS["initial_temp"], 
        SA_PARAMS["cooling_rate"], 
        SA_PARAMS["min_temp"]
    )
    steps_per_m = temp_steps * (thermalization_steps + SA_PARAMS["num_iterations_per_temp"])
    total_steps = steps_per_m * (len(pauli_operators) - 1)

    best_energy = float("inf")
    best_result = None
    all_results = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        task = progress.add_task("[cyan]Отжиг...", total=total_steps)

        for m in range(2, len(pauli_operators) + 1):
            current_ops = pauli_operators[:m]
            initial_theta = generate_shifted_theta(current_ops)

            optimized_theta, energy = simulated_annealing(
                initial_theta=initial_theta,
                pauli_operators=current_ops,
                progress=progress,
                task=task,
                **SA_PARAMS
            )

            all_results.append({
                "m": m,
                "theta": optimized_theta,
                "energy": energy,
                "operators": current_ops
            })

            if energy < best_energy:
                best_energy = energy
                best_result = all_results[-1]

    # Вывод результатов
    if best_result is None:
        console_and_print(console, Panel("[red]Не удалось найти решение[/red]", border_style="red"))
        return

    _, ansatz_symbolic, ansatz_numeric = calculate_ansatz(
        best_result["theta"],
        best_result["operators"]
    )

    console_and_print(console, Panel(ansatz_symbolic,
        title="[bold]Символьное представление анзаца[/]", border_style="green"))

    console_and_print(console, Panel(ansatz_numeric,
        title="[bold]Численное представление анзаца[/]", border_style="purple"))

    console_and_print(console, Panel(f"{best_result['energy']:.6f}",
        title="[bold]Энергия (<0|U†HU|0> для состояния |0...0>)[/]", border_style="green"))

    input('Нажмите Enter для выхода...')


if __name__ == "__main__":
    main()
