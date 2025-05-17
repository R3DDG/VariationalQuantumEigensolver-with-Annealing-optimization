def format_number(num: float | int) -> str:
    """
    Форматирует число с точным определением целочисленных значений
    и подавлением артефактов вычислений с плавающей точкой.

    Args:
        num (float | int): Число.

    Returns:
        str: Отформатированная строка.
    """
    # Проверка на целое число с учетом погрешности
    if abs(num - round(num)) < 1e-15:
        return str(int(round(num)))

    s = f"{num:.14f}".rstrip("0").rstrip(".")

    if s.startswith("."):
        s = "0" + s
    elif s.startswith("-."):
        s = s.replace("-.", "-0.")

    if "." in s:
        int_part, dec_part = s.split(".")
        dec_part = dec_part[:4].ljust(4, "0").rstrip("0")
        s = f"{int_part}.{dec_part}" if dec_part else int_part

    return s
