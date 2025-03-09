from sympy import re as sp_re, im as sp_im
from .format_number import format_number


def format_complex_number(c) -> str:
    """
    Универсальный форматировщик комплексных чисел для SymPy и стандартных типов.
    """
    # Извлечение компонентов через SymPy
    real = float(sp_re(c))
    imag = float(sp_im(c))

    real_str = format_number(real) if abs(real) > 1e-12 else ""
    imag_str = ""

    if abs(imag) > 1e-12:
        abs_imag = abs(imag)
        imag_value = format_number(abs_imag)

        # Специальные случаи для ±1
        if imag_value == "1":
            imag_str = "i" if imag > 0 else "-i"
        else:
            imag_sign = "" if imag > 0 else "-"
            imag_str = f"{imag_sign}{imag_value}i"

    # Сборка результата
    parts = []
    if real_str:
        parts.append(real_str)
    if imag_str:
        parts.append(imag_str)

    if not parts:
        return "0"

    # Корректное объединение компонентов
    result = parts[0]
    for part in parts[1:]:
        if part.startswith("-"):
            result += f"-{part[1:]}"
        else:
            result += f"+{part}"

    # Фикс артефактов форматирования
    return result.replace("+ -", "- ").replace("1i", "i").replace(".0i", "i")
