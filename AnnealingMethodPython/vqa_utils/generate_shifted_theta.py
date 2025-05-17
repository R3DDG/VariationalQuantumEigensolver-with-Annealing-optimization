import numpy as np
from typing import Tuple, List

def generate_shifted_theta(pauli_operators: List[Tuple[complex, List[int]]]) -> np.ndarray:
    """
    Генерирует θ на основе коэффициентов операторов (вектор сдвига).

    Args:
        pauli_operators (List[Tuple[complex, List[int]]]): Операторы Паули.

    Returns:
        np.ndarray: Вектор theta.
    """
    if not pauli_operators:
        return np.array([], dtype=np.float64)
    
    # Извлечение модулей действительных частей
    coeffs = np.array([abs(op[0].real) for op in pauli_operators], dtype=np.float64)
    norm = np.linalg.norm(coeffs)
    if norm < 1e-12:
        return np.zeros(len(coeffs))
    
    # Масштабируем в [0, 2π) и добавляем шум
    scaled = (coeffs / norm) * 2 * np.pi
    return scaled + np.random.normal(0, 0.1, len(scaled))
