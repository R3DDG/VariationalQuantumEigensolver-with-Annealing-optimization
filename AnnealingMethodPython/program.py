import numpy as np  # Для работы с комплексными числами и математическими операциями
import random  # Для генерации случайных чисел
import os  # Для работы с путями и директориями
import sys  # Для работы с системными параметрами и настройки стандартного ввода/вывода
import io  # Для работы с потоками ввода/вывода и настройки кодировки
from rich.console import Console  # Для красивого вывода в консоль
from sympy import I  # Для работы с мнимой единицей
from rich.panel import Panel  # Для панелей с текстом

# Импорт самописных util функций
from annealing_method_utils.console_and_print import console_and_print
from annealing_method_utils.format_number import format_number
from annealing_method_utils.format_complex_number import format_complex_number
from annealing_method_utils.read_hamiltonian_data import read_hamiltonian_data
from annealing_method_utils.create_table import create_table
from annealing_method_utils.get_operator_for_console import get_operator_for_console
from annealing_method_utils.format_ansatz import format_ansatz

# Импорт констант
from annealing_method_constants.file_paths import hamiltonian_file_path
from annealing_method_constants.file_paths import output_file_path

# Устанавливаем кодировку для стандартного вывода
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

def generate_random_theta(m):
    """
    Генерирует массив из m случайных чисел в диапазоне [0, 1).

    :param m: Количество случайных чисел.
    :return: Массив случайных чисел.
    """
    return np.random.rand(m).astype(np.float64)

def Pij(i, j):
    """
    Произведение базисных однокубитных операторов Паули.

    :param i: Индекс первого оператора Паули.
    :param j: Индекс второго оператора Паули.
    :return: Коэффициент и индекс результирующего оператора.
    """
    pauli_map = {
        (1, 2): (I, 3),
        (2, 1): (-I, 3),
        (3, 1): (I, 2),
        (1, 3): (-I, 2),
        (2, 3): (I, 1),
        (3, 2): (-I, 1),
    }
    if i == j:
        return 1, 0
    elif i == 0:
        return 1, j
    elif j == 0:
        return 1, i
    return pauli_map.get((i, j), (1, 0))

def SC(s1, s2):
    """
    Композиция базисных операторов Паули.

    :param s1: Первый оператор Паули в виде списка.
    :param s2: Второй оператор Паули в виде списка.
    :return: Коэффициент и результирующий оператор Паули.
    """
    h = 1
    p = []
    for i in range(len(s1)):
        t, p_i = Pij(s1[i], s2[i])
        h *= t
        p.append(p_i)
    return h, p

def calculate_ansatz(theta, pauli_operators):
    """
    Вычисляет анзац как произведение экспонент операторов Паули, учитывая разложение каждого множителя.

    :param theta: Массив случайных чисел theta.
    :param pauli_operators: Список операторов Паули (списки индексов).
    :return: Символьное представление анзаца и его численное значение.
    """
    # Инициализация результата: начинаем с единичного оператора (все нули) и коэффициента 1.0
    result = {tuple([0] * len(pauli_operators[0])): 1.0}
    
    for t, op in zip(theta, pauli_operators):
        cos_t = np.cos(t)
        sin_t = np.sin(t)
        
        # Создаем два слагаемых: I (нулевой оператор) и sigma_k с коэффициентами
        identity_term = (cos_t, tuple([0] * len(op)))
        pauli_term = (1j * sin_t, tuple(op))
        
        new_result = {}
        # Обрабатываем каждое существующее слагаемое в результате
        for existing_op, existing_coeff in result.items():
            # Умножаем на первое слагаемое (I)
            coeff_i, op_i = identity_term
            h_i, p_i = SC(list(existing_op), list(op_i))
            total_coeff_i = existing_coeff * coeff_i * h_i
            new_op_i = tuple(p_i)
            if new_op_i in new_result:
                new_result[new_op_i] += total_coeff_i
            else:
                new_result[new_op_i] = total_coeff_i
            
            # Умножаем на второе слагаемое (sigma_k)
            coeff_p, op_p = pauli_term
            h_p, p_p = SC(list(existing_op), list(op_p))
            total_coeff_p = existing_coeff * coeff_p * h_p
            new_op_p = tuple(p_p)
            if new_op_p in new_result:
                new_result[new_op_p] += total_coeff_p
            else:
                new_result[new_op_p] = total_coeff_p
        
        result = new_result

    # Формируем U(θ) и U
    return format_ansatz(pauli_operators, result)

def main():
    """Основная функция программы."""
    
    # Инициализация консоли для использования rich
    console = Console(force_terminal=True, color_system="truecolor", record=True)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))   

    # Очистка файла перед началом записи
    if output_file_path.exists():
        output_file_path.unlink()

    # Чтение данных из файла гамильтониана
    try:
        pauli_operators, pauli_strings = read_hamiltonian_data(hamiltonian_file_path)
    except FileNotFoundError:
        console_and_print(
            console, f"[red]Файл {hamiltonian_file_path} не найден.[/red]"
        )
        return

    # Формирование строки гамильтониана
    hamiltonian_str = "H = " + " + ".join(
        [get_operator_for_console(c, i) for c, i in pauli_operators]
    )
    console_and_print(
        console,
        Panel(
            hamiltonian_str,
            title="[bold]Введенный гамильтониан[/bold]",
            border_style="green",
        ),
    )

    # Вывод операторов Паули, полученных из гамильтониана, в виде таблицы
    table_data = [[format_complex_number(c), str(i)] for c, i in pauli_operators]
    console_and_print(
        console,
        create_table(
            [
                {"name": "Коэффициент", "style": "cyan"},
                {"name": "Индекс", "style": "magenta", "justify": "center"},
            ],
            table_data,
            "Операторы Паули",
            "purple",
        ),
    )

    # Проверка наличия операторов Паули
    if not pauli_operators:
        console_and_print(
            console,
            "[red]Файл 'hamiltonian_operators.txt' не содержит операторов Паули.[/red]",
        )
        return

    # Вычисление композиций операторов Паули
    results = [(s1, s2, *SC(s1, s2)) for s1 in pauli_strings for s2 in pauli_strings]
    table_pauli_data = [
        [str(s1), str(s2), str(h).lower(), str(p)] for s1, s2, h, p in results
    ]
    console_and_print(
        console,
        create_table(
            [
                {"name": "Оператор 1", "style": "cyan", "justify": "center"},
                {"name": "Оператор 2", "style": "magenta", "justify": "center"},
                {"name": "Коэффициент", "style": "green", "justify": "center"},
                {"name": "Результат", "style": "red", "justify": "center"},
            ],
            table_pauli_data,
            "Композиции операторов Паули",
            "purple",
        ),
    )

    # Генерация случайных чисел theta
    m = random.randint(
        1, len(pauli_operators) - 1
    )  # m строго меньше количества операторов Паули
    theta = generate_random_theta(m)
    table_theta_data = [
        [str(i), format_number(t)] for i, t in enumerate(theta, start=1)
    ]
    console_and_print(
        console,
        create_table(
            [
                {"name": "Номер θ_i", "style": "cyan"},
                {"name": "Значение θ_i", "style": "magenta", "justify": "center"},
            ],
            table_theta_data,
            "Случайные числа θ_i",
            "green",
        ),
    )

    # Вычисление и вывод анзаца
    ansatz_symbolic, ansatz_numeric = calculate_ansatz(theta, pauli_operators[:m])
    console_and_print(
        console, Panel(ansatz_symbolic, title="[bold]U(θ)[/bold]", border_style="green")
    )
    console_and_print(
        console, Panel(ansatz_numeric, title="[bold]U[/bold]", border_style="purple")
    )
    
    if hasattr(console, 'file') and hasattr(console.file, 'flush'):
        console.file.flush()

if __name__ == "__main__":
    main()
