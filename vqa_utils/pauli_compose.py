from functools import lru_cache
from typing import Tuple
from .multiply_pauli import multiply_pauli

def pauli_compose(s1: tuple, s2: tuple) -> Tuple[complex, tuple]:
    coefficient = 1.0 + 0j
    result = []
    for a, b in zip(s1, s2):
        coeff, idx = multiply_pauli(a, b)
        coefficient *= coeff
        result.append(idx)
        
    return coefficient, tuple(result)
