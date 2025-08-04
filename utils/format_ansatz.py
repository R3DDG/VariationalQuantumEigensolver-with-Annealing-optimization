from .format_complex_number import format_complex_number
from typing import List, Tuple, Dict

def format_ansatz(pauli_operators: List[Tuple[complex, List[int]]], result: Dict[Tuple[int, ...], complex]) -> Tuple[str, str]:
    ansatz_symbolic = "U(θ) = " + " * ".join(
        [
            f"exp(i·θ_{i+1}·{format_complex_number(coeff)}·σ_{''.join(map(str, op))})"
            for i, (coeff, op) in enumerate(pauli_operators)
        ]
    )
    ansatz_numeric = "U = " + " + ".join(
        [
            f"{format_complex_number(c)}·σ_{''.join(map(str, op))}"
            for op, c in result.items()
            if abs(c) > 1e-12
        ]
    )
    return ansatz_symbolic, ansatz_numeric
