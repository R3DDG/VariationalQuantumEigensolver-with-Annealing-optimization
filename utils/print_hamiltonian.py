from rich.console import Console
from rich.panel import Panel
from typing import Tuple, List
from .get_operator_for_console import get_operator_for_console
from .console_and_print import console_and_print

def print_hamiltonian(console: Console, pauli_operators: List[Tuple[complex, List[int]]]) -> None:
   
    hamiltonian_str = "H = " + " + ".join(
        [get_operator_for_console(c, ''.join(map(str, i))) for c, i in pauli_operators]
    )
    console_and_print(
        console,
        Panel(
            hamiltonian_str,
            title="[bold]Введенный гамильтониан[/bold]",
            border_style="green",
        ),
    )
