import numpy as np
from .generate_shifted_theta import generate_shifted_theta
from .calculate_ansatz import calculate_ansatz
from .compute_uhu import compute_uhu
from .calculate_expectation import calculate_expectation

def simulated_annealing(
    initial_theta: np.ndarray,
    pauli_operators: list,
    progress,
    task,
    initial_temp: float = 1000.0,
    cooling_rate: float = 0.99,
    min_temp: float = 1e-5,
    num_iterations_per_temp: int = 500,
    step_size: float = 0.5,
) -> tuple:
    """Алгоритм отжига с термализацией."""
    current_theta = initial_theta.copy()
    best_theta = current_theta.copy()
    best_energy = float("inf")
    rng = np.random.default_rng()
    temp = initial_temp
    thermalization_steps = int(num_iterations_per_temp * 0.2)

    while temp > min_temp:
        # Термализация (можно уменьшить число шагов)
        for _ in range(thermalization_steps):
            current_theta = generate_shifted_theta(pauli_operators)
            ansatz_dict, _, _ = calculate_ansatz(current_theta, pauli_operators)
            uhu_dict = compute_uhu(ansatz_dict, pauli_operators)
            current_energy = calculate_expectation(uhu_dict)
            if current_energy < best_energy:
                best_theta = current_theta.copy()
                best_energy = current_energy
            if progress is not None:
                progress.update(task, advance=1)

        # Основной цикл отжига
        for _ in range(num_iterations_per_temp):
            perturbation = rng.normal(0, step_size*(temp/initial_temp), current_theta.shape)
            neighbor_theta = (current_theta + perturbation) % (2*np.pi)
            ansatz_dict, _, _ = calculate_ansatz(neighbor_theta, pauli_operators)
            uhu_dict = compute_uhu(ansatz_dict, pauli_operators)
            current_energy = calculate_expectation(uhu_dict)
            energy_diff = current_energy - best_energy
            if energy_diff < 0 or rng.random() < np.exp(-energy_diff / temp):
                current_theta = neighbor_theta.copy()
                if current_energy < best_energy:
                    best_theta = current_theta.copy()
                    best_energy = current_energy
            if progress is not None:
                progress.update(task, advance=1)
        temp *= cooling_rate

    return best_theta, best_energy
