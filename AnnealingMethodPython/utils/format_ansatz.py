from .format_complex_number import format_complex_number


def format_ansatz(
    pauli_operators: list[list[int]], result: dict[tuple, complex]
) -> tuple[str, str]:
    """
    Форматирует анзац в символьное и численное представление.

    :param pauli_operators: Список операторов Паули (списки индексов).
    :param result: Словарь с результатами вычислений {оператор: коэффициент}.
    :return: Символьное представление анзаца и его численное значение.
    """
    # Формируем U(θ)
    ansatz_symbolic = "U(θ) = " + " * ".join(
        [
            f"e^(iθ_{i+1}*{format_complex_number(op[0])}*σ_{''.join(map(str, op[1]))})"
            for i, op in enumerate(pauli_operators)
        ]
    )

    # Формируем U
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
