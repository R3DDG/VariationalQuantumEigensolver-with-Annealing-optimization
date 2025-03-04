def format_number(num):
    """
    Форматирует число, убирая лишние нули после запятой, если число целое.

    :param num: Число для форматирования.
    :return: Строковое представление числа.
    """
    if isinstance(num, (int, float)):
        return (
            str(int(num)) if num == int(num) else f"{num:.4f}".rstrip("0").rstrip(".")
        )
    return str(num)
