from rich.console import Console
from typing import Tuple, List, Callable
from .console_and_print import console_and_print
from .create_table import create_table
from .format_complex_number import format_complex_number

def print_composition_table(console: Console, pauli_compose: Callable[[tuple, tuple], Tuple[complex, tuple]], pauli_strings: List[List[int]],) -> None:
    results = []
    for s1 in pauli_strings:
        for s2 in pauli_strings:
            coeff, product = pauli_compose(tuple(s1), tuple(s2))
            results.append((s1, s2, format_complex_number(coeff), product))

    table_data = [[str(s1), str(s2), str(h).lower(), str(p)] for s1, s2, h, p in results]
    console_and_print(
        console,
        create_table(columns=[
                {"name": "Оператор 1", "style": "cyan", "justify": "center"},
                {"name": "Оператор 2", "style": "magenta", "justify": "center"},
                {"name": "Коэффициент", "style": "green", "justify": "center"},
                {"name": "Результат", "style": "red", "justify": "center"},],
            data=table_data,
            title="Композиции операторов Паули",
            border_style="green",),
    )
