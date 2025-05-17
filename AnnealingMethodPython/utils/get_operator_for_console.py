from .format_complex_number import format_complex_number
from typing import Union

def get_operator_for_console(c: Union[complex, float, int], i: str) -> str:
    """
    Формирует строку для красивого вывода оператора Паули.

    Args:
        c (complex|float|int): Коэффициент перед оператором.
        i (str): Индексная строка оператора (например, "03" для I⊗Z).

    Returns:
        str: Строка вида "σ_i" или "c*σ_i" (если коэффициент не равен 1).
    """
    if c == 1:
        return f"σ_{i}"
    else:
        return f"{format_complex_number(c)}*σ_{i}"
