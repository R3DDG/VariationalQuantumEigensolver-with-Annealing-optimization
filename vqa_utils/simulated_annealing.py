import numpy as np
from typing import Any, List, Tuple
from scipy.optimize import dual_annealing
from .generate_neighbor_theta import generate_neighbor_theta
from .calculate_ansatz import calculate_ansatz
from .compute_uhu import compute_uhu
from .calculate_expectation import calculate_expectation

class ProgressTracker:
    def __init__(self, total_iterations: int, progress: Any, task: Any):
        self.total_iterations = total_iterations
        self.current_iteration = 0
        self.progress = progress
        self.task = task
        self.last_update = 0
        self.best_energy = float('inf')
        self.best_theta = None

    def update(self, xk, f, accepted):
        self.current_iteration += 1
        if f < self.best_energy:
            self.best_energy = f
            self.best_theta = xk.copy()
            print(f"Новая лучшая энергия: {self.best_energy:.6f}")
        
        if self.current_iteration - self.last_update > self.total_iterations // 100:
            if self.progress is not None:
                self.progress.update(self.task, advance=1)
            self.last_update = self.current_iteration

def energy_function(theta: np.ndarray, pauli_operators: List[Any], hamiltonian_operators) -> float:
    step_size: float = 0.05
    neighbor_theta = generate_neighbor_theta(theta, step_size)
    ansatz_dict, _, _ = calculate_ansatz(neighbor_theta, pauli_operators)
    uhu_dict = compute_uhu(ansatz_dict, hamiltonian_operators)
    energy = calculate_expectation(uhu_dict)
    if np.isnan(energy) or np.isinf(energy):
        raise ValueError("Получено некорректное значение энергии")
    return energy

def simulated_annealing(
    initial_theta: np.ndarray,
    pauli_operators: List[Any],
    hamiltonian_operators: List[Any],
    progress: Any,
    task: Any,
    initial_temp: float = 50.0,
    cooling_rate: float = 0.98,
    min_temp: float = 1e-6,
    num_iterations_per_temp: int = 38, 
    step_size: float = 0.05,
    bounds: List[Tuple[float, float]] = None) -> Tuple[np.ndarray, float]:

    if bounds is None:
        bounds = [(0, 2*np.pi) for _ in initial_theta]
    total_iterations = num_iterations_per_temp
    progress_tracker = ProgressTracker(total_iterations, progress, task)

    def objective_function(theta):
        return energy_function(theta, pauli_operators, hamiltonian_operators)

    result = dual_annealing(func=objective_function, bounds=bounds, maxiter=num_iterations_per_temp,
        initial_temp=initial_temp,
        callback=progress_tracker.update)

    best_theta = result.x
    best_energy = result.fun
    print(f"Финальная лучшая энергия: {best_energy:.6f}")
    return best_theta, best_energy