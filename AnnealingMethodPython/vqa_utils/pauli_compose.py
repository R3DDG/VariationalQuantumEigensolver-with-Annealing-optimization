from functools import lru_cache
from typing import Tuple, List
from .multiply_pauli import multiply_pauli

@lru_cache(maxsize=4096)
def pauli_compose(s1: tuple, s2: tuple) -> Tuple[complex, tuple]:
    """
    Вычисляет композицию двух операторов Паули покомпонентно.

    Args:
        s1 (tuple): Первый оператор (кортеж индексов).
        s2 (tuple): Второй оператор.

    Returns:
        Tuple[complex, tuple]: (коэффициент, результат)
    """
    coefficient = 1.0
    result = []
    for a, b in zip(s1, s2):
        coeff, idx = multiply_pauli(a, b)
        coefficient *= coeff
        result.append(idx)
    return coefficient, tuple(result)
