from typing import Tuple
from constants.pauli import PAULI_MAP

def multiply_pauli(i: int, j: int) -> Tuple[complex, int]:
    """
    Вычисляет произведение базисных операторов Паули.
    Возвращает: (коэффициент, индекс результата)
    """
    if i == j:
        return (1, 0)
    if i == 0:
        return (1, j)
    if j == 0:
        return (1, i)
    return PAULI_MAP.get((i, j), (1, 0))