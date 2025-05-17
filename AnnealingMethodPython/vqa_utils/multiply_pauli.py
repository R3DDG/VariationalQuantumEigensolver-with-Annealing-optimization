from typing import Tuple
from constants.pauli import PAULI_MAP

def multiply_pauli(i: int, j: int) -> Tuple[complex, int]:
    """
    Перемножает два базисных оператора Паули.

    Args:
        i (int): Первый индекс (0=I, 1=X, 2=Y, 3=Z).
        j (int): Второй индекс (0=I, 1=X, 2=Y, 3=Z).

    Returns:
        Tuple[complex, int]: Коэффициент и индекс результата.
    """
    if i == j:
        return (1, 0)
    if i == 0:
        return (1, j)
    if j == 0:
        return (1, i)
    return PAULI_MAP.get((i, j), (1, 0))
