from .format_complex_number import format_complex_number
from typing import Union

def get_operator_for_console(c: Union[complex, float, int], i: str) -> str:
    """
    Форматирует оператор Паули для красивого вывода в консоль.

    Args:
        c (complex | float | int): Коэффициент оператора Паули.
        i (str): Строка оператора Паули.

    Returns:
        str: Отформатированная строка.
    """
    if c == 1:
        return f"σ_{i}"
    else:
        return f"{format_complex_number(c)}*σ_{i}"
