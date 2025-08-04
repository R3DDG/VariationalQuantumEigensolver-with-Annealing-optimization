import numpy as np
from typing import Tuple, List, Dict
from utils.format_ansatz import format_ansatz
from .pauli_compose import pauli_compose

def calculate_ansatz(theta: np.ndarray, pauli_operators: List[Tuple[complex, List[int]]]) -> Tuple[Dict[Tuple[int, ...], complex], str, str]:
    operator_length = len(pauli_operators[0][1])
    result: Dict[Tuple[int, ...], complex] = {tuple([0]*operator_length): 1.0 + 0j}
    
    if len(theta) != len(pauli_operators):
        raise ValueError("Размеры theta и pauli_operators должны совпадать")

    for i, (coeff, op) in enumerate(pauli_operators):
        angle = theta[i] * coeff
        temp_result = {}
        
        for existing_op, existing_coeff in result.items():
            cos_t = np.cos(angle)

            if existing_op in temp_result:
                temp_result[existing_op] += existing_coeff * cos_t
            else:
                temp_result[existing_op] = existing_coeff * cos_t

            compose_coeff, compose_op = pauli_compose(existing_op, tuple(op))
            sin_t = np.sin(angle)
            new_coeff = 1j * existing_coeff * sin_t * compose_coeff
            
            if compose_op in temp_result:
                temp_result[compose_op] += new_coeff
            else:
                temp_result[compose_op] = new_coeff
        
        result = temp_result
    
    symbolic_str, numeric_str = format_ansatz(pauli_operators, result)
    return result, symbolic_str, numeric_str