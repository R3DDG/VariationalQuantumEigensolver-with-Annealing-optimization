import numpy as np  # Для работы с комплексными числами и математическими операциями
from pathlib import Path  # Для работы с файловой системой
import random  # Для генерации случайных чисел
import os  # Для работы с путями и директориями
import sys  # Для работы с системными параметрами и настройки стандартного ввода/вывода
import io  # Для работы с потоками ввода/вывода и настройки кодировки
from rich.console import Console  # Для красивого вывода в консоль
from rich.table import Table  # Для создания таблиц
from rich.panel import Panel  # Для панелей с текстом
from rich import box  # Для стилизации таблиц
from sympy import Mul, I, re, im  # Для работы с математическими символами и мнимой единицей

# Устанавливаем кодировку для стандартного вывода
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Инициализация консоли для использования rich
console = Console(force_terminal=True, color_system="truecolor")

def generate_random_theta(m: int) -> list[float]:
    """
    Генерирует список из m случайных чисел в диапазоне [0, 1).

    :param m: Количество случайных чисел.
    :return: Список случайных чисел.
    """
    return [random.random() for _ in range(m)]

def read_file_lines(file_path: str | Path, ignore_comments: bool = True) -> list[str]:
    """
    Читает строки из файла, игнорируя комментарии (строки, начинающиеся с '#').

    :param file_path: Путь к файлу.
    :param ignore_comments: Игнорировать строки, начинающиеся с '#'.
    :return: Список строк.
    :raises FileNotFoundError: Если файл не найден.
    """
    file_path = Path(file_path) if not isinstance(file_path, Path) else file_path
    if not file_path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if not (ignore_comments and line.strip().startswith('#'))]

def format_number(num: int | float) -> str:
    """
    Форматирует число, убирая лишние нули после запятой, если число целое.

    :param num: Число для форматирования.
    :return: Строковое представление числа.
    """
    if isinstance(num, (int, float)):
        return str(int(num)) if num == int(num) else f"{num:.4f}".rstrip('0').rstrip('.')
    return str(num)

def format_complex_number(c: int | float | complex | Mul) -> str:
    """
    Преобразует комплексное число или символьное выражение в строку в удобочитаемом формате.

    :param c: Комплексное число или символьное выражение.
    :return: Строковое представление комплексного числа.
    """
    if isinstance(c, (int, float, complex)):
        real_part = format_number(c.real) if c.real != 0 else ""
        imag_part = format_number(c.imag) + "i" if c.imag != 0 else ""
    elif isinstance(c, Mul):
        real_part = format_number(float(re(c))) if re(c) != 0 else ""
        imag_part = format_number(float(im(c))) + "i" if im(c) != 0 else ""
    else:
        real_part = str(c)
        imag_part = ""

    if not real_part and not imag_part:
        return "0"
    return f"{real_part}{('+' if imag_part and imag_part[0] != '-' else '')}{imag_part}"

def Pij(i: int, j: int) -> tuple[int | complex, int]:
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

def SC(s1: list[int], s2: list[int]) -> tuple[int | complex, list[int]]:
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

def read_hamiltonian_data(file_path: str | Path) -> tuple[list[tuple[complex, int]], list[list[int]]]:
    """
    Читает данные из файла hamiltonian_operators.txt и возвращает два списка:
    - Список термов гамильтониана (коэффициент, индекс).
    - Список операторов Паули.

    :param file_path: Путь к файлу.
    :return: (hamiltonian_terms, pauli_operators)
    :raises FileNotFoundError: Если файл не найден.
    """
    lines = read_file_lines(file_path, ignore_comments=False)
    hamiltonian_terms = []
    pauli_operators = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) == 3:
            real_part, imag_part, index = float(parts[0]), float(parts[1]), int(parts[2])
            coefficient = np.complex128(real_part + imag_part * 1j)
            if coefficient != 0:
                hamiltonian_terms.append((coefficient, index))
            pauli_operators.append([int(c) for c in parts[2]])
    return hamiltonian_terms, pauli_operators

def create_table(
    columns: list[dict[str, str]], data: list[list[str]], title: str, border_style: str = "yellow"
) -> Panel:
    """
    Создает таблицу с заданными колонками и данными.

    :param columns: Список словарей с описанием колонок.
    :param data: Данные для таблицы.
    :param title: Заголовок таблицы.
    :param border_style: Стиль границы таблицы.
    :return: Панель с таблицей.
    """
    table = Table(box=box.ROUNDED, border_style="yellow")
    for col in columns:
        table.add_column(col["name"], justify=col.get("justify", "default"), style=col.get("style", ""))
    for row in data:
        table.add_row(*row)
    return Panel(table, title=title, border_style=border_style)

def calculate_ansatz(theta: list[float], pauli_operators: list[list[int]]) -> tuple[str, str]:
    """
    Вычисляет анзац по заданной формуле, перемножая скобки и упрощая результат.

    :param theta: Список случайных чисел theta.
    :param pauli_operators: Список операторов Паули (списки индексов).
    :return: Символьное представление анзаца и его численное значение.
    """
    # Инициализация результата как словаря {оператор: коэффициент}
    result = {tuple([0] * len(pauli_operators[0])): 1.0}  # Начинаем с единичного оператора (σ_000...)

    # Перемножаем все члены анзаца
    for t, op in zip(theta, pauli_operators):
        cos_t = np.cos(t)
        sin_t = np.sin(t)
        current_op = tuple(op)
        current_coeff = cos_t + 1j * sin_t

        # Обновляем результат
        new_result = {}
        for existing_op, existing_coeff in result.items():
            h, p = SC(list(existing_op), list(current_op))
            new_op = tuple(p)
            new_coeff = existing_coeff * current_coeff * h
            if new_op in new_result:
                new_result[new_op] += new_coeff
            else:
                new_result[new_op] = new_coeff
        result = new_result

    # Формируем U(θ) и U
    ansatz_symbolic = "U(θ) = " + " * ".join(
        [f"e^(iθ_{i+1}σ_{''.join(map(str, op))})" for i, op in enumerate(pauli_operators)]
    )
    ansatz_numeric = "U = " + " + ".join(
        [f"{format_complex_number(c)}*σ_{''.join(map(str, op))}" for op, c in result.items()]
    )

    return ansatz_symbolic, ansatz_numeric

def main() -> None:
    """Основная функция программы."""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Пути к файлам
    hamiltonian_file_path = Path("params/hamiltonian_operators.txt")

    # Чтение данных из файла гамильтониана
    try:
        hamiltonian_terms, pauli_operators = read_hamiltonian_data(hamiltonian_file_path)
    except FileNotFoundError:
        console.print(f"[red]Файл {hamiltonian_file_path} не найден.[/red]")
        return

    # Формирование строки гамильтониана
    hamiltonian_str = "H = " + " + ".join([f"{format_complex_number(c)}*σ_{i}" for c, i in hamiltonian_terms])
    console.print(Panel(hamiltonian_str, title="[bold]Введенный гамильтониан[/bold]", border_style="green"))

    # Вывод термов гамильтониана в виде таблицы
    table_data = [[format_complex_number(c), str(i)] for c, i in hamiltonian_terms]
    console.print(
        create_table(
            [
                {"name": "Коэффициент", "style": "cyan"},
                {"name": "Индекс", "style": "magenta", "justify": "center"},
            ],
            table_data,
            "Термы гамильтониана",
            "purple",
        )
    )

    # Генерация случайных чисел theta
    m = random.randint(1, len(pauli_operators) - 1)  # m строго меньше количества операторов Паули
    theta = generate_random_theta(m)
    table_theta_data = [[str(i), format_number(t)] for i, t in enumerate(theta, start=1)]
    console.print(
        create_table(
            [
                {"name": "Номер θ_i", "style": "cyan"},
                {"name": "Значение θ_i", "style": "magenta", "justify": "center"},
            ],
            table_theta_data,
            "Случайные числа θ_i",
            "green",
        )
    )

    # Проверка наличия операторов Паули
    if not pauli_operators:
        console.print("[red]Файл 'hamiltonian_operators.txt' не содержит операторов Паули.[/red]")
        return

    # Вычисление композиций операторов Паули
    results = [(s1, s2, *SC(s1, s2)) for s1 in pauli_operators for s2 in pauli_operators]
    table_pauli_data = [[str(s1), str(s2), str(h).lower(), str(p)] for s1, s2, h, p in results]
    console.print(
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
        )
    )

    # Вычисление и вывод анзаца
    ansatz_symbolic, ansatz_numeric = calculate_ansatz(theta, pauli_operators[:m])
    console.print(Panel(ansatz_symbolic, title="[bold]U(θ)[/bold]", border_style="green"))
    console.print(Panel(ansatz_numeric, title="[bold]U[/bold]", border_style="purple"))

if __name__ == "__main__":
    main()
