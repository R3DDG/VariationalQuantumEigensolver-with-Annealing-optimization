from sympy import Mul, re, im # Для работы с математическими символами
from .format_number import format_number

def format_complex_number(c: int | float | complex | Mul) -> str:
    """
    Преобразует комплексное число или символьное выражение в строку в удобочитаемом формате.

    :param c: Комплексное число или символьное выражение.
    :return: Строковое представление комплексного числа.
    """
    if isinstance(c, (int, float, complex)):
        real_part = format_number(c.real) if c.real != 0 else ""
        imag_part = format_number(c.imag) + "i" if c.imag != 0 else ""
    elif isinstance(c, Mul):
        real_part = format_number(float(re(c))) if re(c) != 0 else ""
        imag_part = format_number(float(im(c))) + "i" if im(c) != 0 else ""
    else:
        real_part = str(c)
        imag_part = ""

    if not real_part and not imag_part:
        return "0"
    return f"{real_part}{('+' if imag_part and imag_part[0] != '-' else '')}{imag_part}"