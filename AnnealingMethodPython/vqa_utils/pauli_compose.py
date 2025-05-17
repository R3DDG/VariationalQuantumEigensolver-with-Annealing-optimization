from functools import lru_cache
from typing import Tuple, List
from .multiply_pauli import multiply_pauli

@lru_cache(maxsize=4096)
def pauli_compose(s1: List[int], s2: List[int]) -> Tuple[complex, Tuple[int, ...]]:
    """
    Вычисляет композицию двух операторов Паули.
    Возвращает: (коэффициент, результирующий оператор)
    """
    s1_tuple = tuple(s1)
    s2_tuple = tuple(s2)
    coefficient = 1.0
    result = []
    for a, b in zip(s1_tuple, s2_tuple):
        coeff, idx = multiply_pauli(a, b)
        coefficient *= coeff
        result.append(idx)
    return coefficient, tuple(result)
