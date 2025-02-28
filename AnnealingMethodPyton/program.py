# Импортируем необходимые библиотеки
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
from sympy import symbols, I  # Для работы с математическими символами и мнимой единицей

# Устанавливаем кодировку для стандартного вывода
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Инициализация консоли для использования rich
console = Console(force_terminal=True, color_system="truecolor")

def generate_random_theta(m):
    """
    Генерирует список из m случайных чисел в диапазоне [0, 1).

    :param m: Количество случайных чисел.
    :return: Список случайных чисел.
    """
    return [random.random() for _ in range(m)]

def read_coefficients_from_file(file_path):
    """
    Читает коэффициенты из файла и возвращает их в виде списка чисел.

    :param file_path: Путь к файлу с коэффициентами.
    :return: Список коэффициентов.
    :raises FileNotFoundError: Если файл не найден.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    return [float(line.strip()) for line in file_path.read_text().splitlines()]

def format_number(num):
    """
    Форматирует число, убирая лишние нули после запятой, если число целое.

    :param num: Число для форматирования.
    :return: Строковое представление числа.
    """
    if isinstance(num, (int, float)):
        return str(int(num)) if num == int(num) else f"{num:.4f}".rstrip('0').rstrip('.')
    return str(num)

def format_complex_number(c):
    """
    Преобразует комплексное число в строку в удобочитаемом формате.

    :param c: Комплексное число (тип numpy.complex128).
    :return: Строковое представление комплексного числа.
    """
    real_part = format_number(c.real) if c.real != 0 else ""
    imag_part = ""
    if c.imag != 0:
        imag_part = "i" if c.imag == 1 else "-i" if c.imag == -1 else f"{format_number(c.imag)}i"

    if not real_part and not imag_part:
        return "0"
    elif not real_part:
        return imag_part
    elif not imag_part:
        return real_part
    else:
        return f"{imag_part}+{real_part}" if c.imag > 0 else f"{imag_part[1:]}-{real_part}"

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
        (3, 2): (-I, 1)
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

def read_hamiltonian_operators(file_path):
    """
    Чтение операторов Паули из файла hamiltonian_operators.txt.

    :param file_path: Путь к файлу.
    :return: Список операторов Паули.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    operators = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) != 3:
                continue  # Пропускаем строки с неправильным форматом
            operators.append([int(c) for c in parts[2]])
    return operators

def main():
    """
    Основная функция программы.
    """
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Определяем символы
    sigma = symbols('σ')
    thetaSymbol = symbols('θ')

    # Пути к файлам
    hamiltonian_file_path = Path("params/hamiltonian_operators.txt")  # Файл с термами гамильтониана
    coefficients_file_path = Path("params/coefficients.txt")  # Файл с коэффициентами

    # Чтение данных из файла гамильтониана
    hamiltonian_terms = []  # Список для хранения термов гамильтониана
    try:
        with open(hamiltonian_file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) != 3:
                    console.print(f"[red]Неверный формат строки: {line}[/red]")
                    continue
                real_part, imag_part, index = float(parts[0]), float(parts[1]), int(parts[2])
                coefficient = np.complex128(real_part + imag_part * 1j)
                if coefficient != 0:
                    hamiltonian_terms.append((coefficient, index))
    except FileNotFoundError:
        console.print(f"[red]Файл {hamiltonian_file_path} не найден.[/red]")
        return

    # Формирование строки гамильтониана
    hamiltonian_str = "H = " + " + ".join([f"{format_complex_number(c)}*{sigma}_{i}" for c, i in hamiltonian_terms])
    console.print(Panel(f"{hamiltonian_str}", title="[bold]Введенный гамильтониан[/bold]", border_style="green"))

    # Вывод термов гамильтониана в виде таблицы
    table = Table(box=box.ROUNDED, border_style="yellow")
    table.add_column("Коэффициент", justify="default", style="cyan")
    table.add_column("Индекс", justify="center", style="magenta")
    for c, i in hamiltonian_terms:
        table.add_row(format_complex_number(c), str(i))
    console.print(Panel(table, title="Термы гамильтониана", border_style="purple"))

    # Генерация случайных чисел theta
    theta = generate_random_theta(5)  # Генерируем 5 случайных чисел

    # Вывод случайных чисел theta
    table_theta = Table(box=box.ROUNDED, border_style="yellow")
    table_theta.add_column(f"Номер {thetaSymbol}_i", justify="default", style="cyan")
    table_theta.add_column(f"Значение {thetaSymbol}_i", justify="center", style="magenta")
    for i, t in enumerate(theta, start=1):
        table_theta.add_row(str(i), format_number(t))
    console.print(Panel(table_theta, title="Случайные числа θ_i", border_style="green"))

    # Чтение коэффициентов из файла
    try:
        coefficients = read_coefficients_from_file(coefficients_file_path)
        if len(coefficients) != len(theta):
            console.print("[red]Ошибка: количество коэффициентов не совпадает с количеством переменных θ.[/red]")
            return
    except FileNotFoundError as e:
        console.print(f"[red]{e}[/red]")
        return

    # Чтение операторов Паули из файла hamiltonian_operators.txt
    try:
        pauli_operators = read_hamiltonian_operators(hamiltonian_file_path)
        if not pauli_operators:
            console.print("[red]Файл 'hamiltonian_operators.txt' не содержит операторов Паули.[/red]")
            return
    except FileNotFoundError as e:
        console.print(f"[red]{e}[/red]")
        return

    # Вычисление композиций операторов Паули
    results = []
    for i, s1 in enumerate(pauli_operators):
        for j, s2 in enumerate(pauli_operators):
            h, p = SC(s1, s2)
            results.append((s1, s2, h, p))

    # Вывод результатов композиции операторов Паули
    table_pauli = Table(box=box.ROUNDED, border_style="yellow")
    table_pauli.add_column("Оператор 1", justify="center", style="cyan")
    table_pauli.add_column("Оператор 2", justify="center", style="magenta")
    table_pauli.add_column("Коэффициент", justify="center", style="green")
    table_pauli.add_column("Результат", justify="center", style="red")
    for s1, s2, h, p in results:
        table_pauli.add_row(str(s1), str(s2), str(h).lower(), str(p))
    console.print(Panel(table_pauli, title="Композиции операторов Паули", border_style="purple"))

# Точка входа в программу
if __name__ == "__main__":
    main()
