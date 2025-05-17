from .format_complex_number import format_complex_number
from typing import List, Tuple, Dict

def format_ansatz(
    pauli_operators: List[Tuple[complex, List[int]]], result: Dict[Tuple[int, ...], complex]
) -> Tuple[str, str]:
    """
    Форматирует вариационный анзац в символьное и численное представление.

    Args:
        pauli_operators (List[Tuple[complex, List[int]]]): Список операторов Паули для анзаца,
            где каждый оператор представлен кортежем из коэффициента и вектора индексов.
        result (Dict[Tuple[int, ...], complex]): Разложение анзаца после экспоненцирования
            по базису Паули (ключ: вектор индексов, значение: коэффициент).

    Returns:
        Tuple[str, str]: Строки символьного (произведение экспонент) и численного (разложение) представления.

    Символьное представление важно для понимания структуры унитарного оператора:
        U(θ) = exp(i·θ₁·c₁·σ₁) * exp(i·θ₂·c₂·σ₂) * ...

    Численное разложение полезно для анализа конечного состояния оператора:
        U = α₀·I + α₁·σ₁ + α₂·σ₂ + ...
    """
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
