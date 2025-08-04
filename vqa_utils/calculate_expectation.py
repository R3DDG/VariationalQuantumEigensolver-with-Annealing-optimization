from typing import Dict, Tuple

def calculate_expectation(uhu_dict: Dict[Tuple[int, ...], complex]) -> float:
    energy = 0.0
    
    for pauli_indices, coefficient in uhu_dict.items():
        if all(index in (0, 3) for index in pauli_indices):
            energy += coefficient.real

    return energy