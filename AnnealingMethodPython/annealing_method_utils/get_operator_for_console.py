from .format_complex_number import format_complex_number

def get_operator_for_console(c, i):
    """
    Функция создана для 'красивого' вывода оператора Паули в консоль.
    Избегает ситуаций, когда у нас выводится конструкция вида '1*σ'

    :param c: Коэффициент оператора Паули.
    :param i: Строка оператора Паули.
    :return: Отформатированную строку.
    """
    if c == 1:
        return f"σ_{i}"
    else:
        return f"{format_complex_number(c)}*σ_{i}"
