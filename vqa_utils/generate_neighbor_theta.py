import numpy as np

def generate_neighbor_theta(current_theta: np.ndarray, step_size: float = 0.05) -> np.ndarray:
    perturbation = np.random.normal(scale=step_size, size=current_theta.shape)
    
    return (current_theta + perturbation) % (2*np.pi)
