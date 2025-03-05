from rich.console import Console  # Для красивого вывода в консоль
from rich.panel import Panel  # Для панелей с текстом
from typing import Tuple, List
from .get_operator_for_console import get_operator_for_console
from .console_and_print import console_and_print

def print_hamiltonian(
    console: Console, pauli_operators: List[Tuple[complex, List[int]]]
) -> None:
    """Выводит представление гамильтониана в консоль."""
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
