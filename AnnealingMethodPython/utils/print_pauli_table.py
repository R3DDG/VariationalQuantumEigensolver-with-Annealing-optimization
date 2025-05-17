from rich.console import Console
from typing import Tuple, List
from .format_complex_number import format_complex_number
from .console_and_print import console_and_print
from .create_table import create_table

def print_pauli_table(
    console: Console, pauli_operators: List[Tuple[complex, List[int]]]
) -> None:
    """
    Выводит таблицу всех операторов Паули из гамильтониана.

    Args:
        console (Console): rich.Console для вывода.
        pauli_operators (List[Tuple[complex, List[int]]]): Список операторов Паули с коэффициентами.
    """
    table_data = [[format_complex_number(c), str(i)] for c, i in pauli_operators]
    console_and_print(
        console,
        create_table(
            columns=[
                {"name": "Коэффициент", "style": "cyan"},
                {"name": "Индекс", "style": "magenta", "justify": "center"},
            ],
            data=table_data,
            title="Операторы Паули",
            border_style="purple",
        ),
    )
