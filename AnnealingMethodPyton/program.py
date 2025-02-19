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
from sympy import symbols  # Для работы с математическими символами

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
        if num == int(num):  # Проверяем, является ли число целым
            return str(int(num))
        else:
            return f"{num:.4f}".rstrip('0').rstrip('.')  # Убираем лишние нули
    return str(num)

def format_complex_number(c):
    """
    Преобразует комплексное число в строку в удобочитаемом формате.

    :param c: Комплексное число (тип numpy.complex128).
    :return: Строковое представление комплексного числа.
    """
    # Обрабатываем действительную часть
    real_part = format_number(c.real) if c.real != 0 else ""
    # Обрабатываем мнимую часть
    imag_part = ""
    if c.imag != 0:
        if c.imag == 1:
            imag_part = "i"
        elif c.imag == -1:
            imag_part = "-i"
        else:
            imag_part = f"{format_number(c.imag)}i"

    # Формируем итоговую строку
    if not real_part and not imag_part:
        return "0"  # Если обе части нулевые
    elif not real_part:
        return imag_part  # Если действительная часть нулевая
    elif not imag_part:
        return real_part  # Если мнимая часть нулевая
    else:
        return f"{imag_part}+{real_part}" if c.imag > 0 else f"{imag_part[1:]}-{real_part}"  # Общий случай

def main():
    """
    Основная функция программы.
    """

    # Меняем рабочую директорию на ту, где находится программа для правильного чтения файлов
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
                parts = line.strip().split()  # Разбиваем строку на части
                if len(parts) != 3:
                    console.print(f"[red]Неверный формат строки: {line}[/red]")
                    continue  # Пропускаем строки с неправильным форматом

                # Извлекаем действительную и мнимую части, а также индекс
                real_part = float(parts[0])
                imag_part = float(parts[1])
                index = int(parts[2])

                # Создаем комплексное число с использованием numpy
                coefficient = np.complex128(real_part + imag_part * 1j)
                if coefficient != 0:  # Если коэффициент не нулевой, добавляем в список
                    hamiltonian_terms.append((coefficient, index))
    except FileNotFoundError:
        console.print(f"[red]Файл {hamiltonian_file_path} не найден.[/red]")
        return

    # Формирование строки гамильтониана
    hamiltonian_str = "H = " + " + ".join([f"{format_complex_number(c)}*{sigma}_{i}" for c, i in hamiltonian_terms])
    console.print(Panel(f"[bold]Введенный гамильтониан:[/bold]\n{hamiltonian_str}", title="Гамильтониан", border_style="green"))

    # Вывод термов гамильтониана в виде таблицы
    table = Table(title="Термы гамильтониана", box=box.ROUNDED, border_style="yellow")
    table.add_column("Коэффициент", justify="center", style="cyan")
    table.add_column("Индекс", justify="center", style="magenta")
    for c, i in hamiltonian_terms:
        table.add_row(format_complex_number(c), str(i))
    console.print(table)

    # Генерация случайных чисел theta
    theta = generate_random_theta(5)  # Генерируем 5 случайных чисел

    # Вывод случайных чисел theta
    console.print(Panel("[bold]Случайные числа θ_i:[/bold]", title="Генерация θ", border_style="blue"))
    for i, t in enumerate(theta, start=1):
        console.print(f"{thetaSymbol}_{i}: [bold]{format_number(t)}[/bold]")  # Используем функцию format_number

    # Чтение коэффициентов из файла
    try:
        coefficients = read_coefficients_from_file(coefficients_file_path)
        if len(coefficients) != len(theta):
            console.print("[red]Ошибка: количество коэффициентов не совпадает с количеством переменных θ.[/red]")
            return  # Завершаем программу, если количество не совпадает
    except FileNotFoundError as e:
        console.print(f"[red]{e}[/red]")
        return


# Точка входа в программу
if __name__ == "__main__":
    main()

# Задание
# 1. Используя файлы со встречи 19.02.2024 доработать функцию
