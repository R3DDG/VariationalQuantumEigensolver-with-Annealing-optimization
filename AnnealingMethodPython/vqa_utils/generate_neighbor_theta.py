import numpy as np

def generate_neighbor_theta(
    current_theta: np.ndarray, step_size: float = 0.1
) -> np.ndarray:
    """
    Генерирует новое состояние θ, добавляя нормальный шум
    с заданной дисперсией, и приводит все значения к диапазону [0, 2π).

    Args:
        current_theta (np.ndarray): Текущий вектор параметров.
        step_size (float): Стандартное отклонение для гауссового шума.

    Returns:
        np.ndarray: Новый вектор параметров.
    """
    perturbation = np.random.normal(scale=step_size, size=current_theta.shape)
    return (current_theta + perturbation) % (2 * np.pi)
