import numpy as np
from typing import List, Tuple

def generate_shifted_theta(pauli_operators: List[Tuple[complex, List[int]]]) -> np.ndarray:
    """
    Генерирует начальный вектор θ для анзаца, масштабируя его пропорционально
    модулям коэффициентов операторов Паули.

    Args:
        pauli_operators (List[Tuple[complex, List[int]]]): Операторы Паули.

    Returns:
        np.ndarray: Начальный вектор θ (размер соответствует числу операторов).
    """
    if not pauli_operators:
        return np.array([], dtype=np.float64)
    # Используем модуль коэффициента (абсолютная величина, чтобы избежать ошибок для комплексных коэффициентов)
    coeffs = np.array([abs(op[0]) for op in pauli_operators], dtype=np.float64)
    norm = np.linalg.norm(coeffs)
    if norm < 1e-12:
        return np.zeros(len(coeffs))
    # Масштабируем на диапазон [0, 2π) и добавляем небольшой случайный шум
    scaled = (coeffs / norm) * 2 * np.pi
    return scaled + np.random.normal(0, 0.1, len(scaled))
