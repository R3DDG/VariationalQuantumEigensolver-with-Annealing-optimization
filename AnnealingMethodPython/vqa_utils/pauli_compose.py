from functools import lru_cache
from typing import Tuple

from .multiply_pauli import multiply_pauli

@lru_cache(maxsize=4096)
def pauli_compose(s1: tuple, s2: tuple) -> Tuple[complex, tuple]:
    """
    Перемножает два оператора Паули, заданных покубитно.

    Args:
        s1 (tuple): Индексы первого оператора (например, (0,3) для I⊗Z).
        s2 (tuple): Индексы второго оператора.

    Returns:
        Tuple[complex, tuple]: Коэффициент и индексы результата.
    """
    coefficient = 1.0
    result = []
    for a, b in zip(s1, s2):
        coeff, idx = multiply_pauli(a, b)
        coefficient *= coeff
        result.append(idx)
    return coefficient, tuple(result)
