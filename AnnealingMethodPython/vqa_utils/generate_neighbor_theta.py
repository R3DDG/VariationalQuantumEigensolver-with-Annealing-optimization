import numpy as np

def generate_neighbor_theta(
    current_theta: np.ndarray, step_size: float = 0.1
) -> np.ndarray:
    """
    Генерирует соседнее решение, добавляя случайный шум к текущему theta.

    Args:
        current_theta (np.ndarray): Текущий вектор theta.
        step_size (float): Размер шага.

    Returns:
        np.ndarray: Новый вектор theta.
    """
    perturbation = np.random.normal(scale=step_size, size=current_theta.shape)
    return np.clip(current_theta + perturbation, 0.0, 1.0)
