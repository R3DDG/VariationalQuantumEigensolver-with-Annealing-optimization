import numpy as np  # Для работы с комплексными числами и математическими операциями
from rich.console import Console  # Для красивого вывода в консоль
from .format_number import format_number
from .console_and_print import console_and_print
from .create_table import create_table


def print_theta_table(console: Console, theta: np.ndarray) -> None:
    """Выводит таблицу значений theta."""
    table_data = [[str(i), format_number(t)] for i, t in enumerate(theta, start=1)]
    console_and_print(
        console,
        create_table(
            columns=[
                {"name": "Номер θ_i", "style": "cyan"},
                {"name": "Значение θ_i", "style": "magenta", "justify": "center"},
            ],
            data=table_data,
            title="Случайные числа θ_i",
            border_style="purple",
        ),
    )
