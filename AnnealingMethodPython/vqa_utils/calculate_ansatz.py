import numpy as np
from typing import Tuple, List, Dict, Any
from utils.format_ansatz import format_ansatz
from .pauli_compose import pauli_compose

def calculate_ansatz(
    theta: np.ndarray, pauli_operators: List[Tuple[complex, List[int]]]
) -> Tuple[Dict[Tuple[int, ...], complex], str, str]:
    """
    Вычисляет анзац в виде произведения экспонент операторов Паули.

    Args:
        theta (np.ndarray): Вектор параметров θ.
        pauli_operators (List[Tuple[complex, List[int]]]): Операторы Паули.

    Returns:
        Tuple[Dict[Tuple[int, ...], complex], str, str]: 
            - словарь операторов,
            - символьное представление,
            - численное представление.
    """
    operator_length = len(pauli_operators[0][1])
    result: Dict[Tuple[int, ...], complex] = {tuple([0]*operator_length): 1.0}

    for t, (_, op) in zip(theta, pauli_operators):
        cos_t = np.cos(t)
        sin_t = np.sin(t)
        new_result: Dict[Tuple[int, ...], complex] = {}
        op_tuple = tuple(op)
        for existing_op, existing_coeff in result.items():
            # cos(θ) * I
            new_result[existing_op] = new_result.get(existing_op, 0) + existing_coeff * cos_t
            # i*sin(θ)*σ
            compose_coeff, compose_op = pauli_compose(tuple(existing_op), tuple(op_tuple))
            final_coeff = existing_coeff * 1j * sin_t * compose_coeff
            new_result[compose_op] = new_result.get(compose_op, 0) + final_coeff
        result = new_result
        
    symbolic_str, numeric_str = format_ansatz(pauli_operators, result)
    return result, symbolic_str, numeric_str
