import numpy as np
from typing import List, Tuple

def generate_shifted_theta(pauli_operators: List[Tuple[complex, List[int]]]) -> np.ndarray:
    if not pauli_operators:
        return np.array([], dtype=np.float64)
    coeffs = np.array([abs(op[0]) for op in pauli_operators], dtype=np.float64)
    norm = np.linalg.norm(coeffs, ord=np.inf)
    if norm < 1e-10:
        return np.zeros(len(coeffs))
    scaled = ((coeffs*(2 * np.pi)) / norm) % (2 * np.pi)

    return scaled + np.random.normal(0, 0.1, len(scaled))
