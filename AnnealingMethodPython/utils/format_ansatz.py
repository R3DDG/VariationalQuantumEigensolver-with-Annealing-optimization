from .format_complex_number import format_complex_number
from typing import List, Dict, Tuple

def format_ansatz(
    pauli_operators: List[List[int]], result: Dict[tuple, complex]
) -> Tuple[str, str]:
    """
    Форматирует анзац в символьное и численное представление.

    Args:
        pauli_operators (List[List[int]]): Список операторов Паули (списки индексов).
        result (Dict[tuple, complex]): Словарь с результатами вычислений {оператор: коэффициент}.

    Returns:
        Tuple[str, str]: Символьное и численное представления анзаца.
    """
    # Формируем U(θ) символьно
    ansatz_symbolic = "U(θ) = " + " * ".join(
        [
            f"e^(iθ_{i+1}*{format_complex_number(op[0])}*σ_{''.join(map(str, op[1]))})"
            for i, op in enumerate(pauli_operators)
        ]
    )

    # Формируем U численно
    ansatz_numeric = "U = " + " + ".join(
        [
            f"{format_complex_number(c)}*{format_complex_number(op[0])}*σ_{''.join(map(str, op[1:]))}"
            if isinstance(op, (list, tuple))
            and len(op) > 1
            and isinstance(op[0], complex)
            else f"{format_complex_number(c)}*σ_{''.join(map(str, op))}"
            for op, c in result.items()
        ]
    )

    return ansatz_symbolic, ansatz_numeric
