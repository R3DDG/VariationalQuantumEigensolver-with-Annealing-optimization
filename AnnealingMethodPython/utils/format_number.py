def format_number(num: float | int) -> str:
    """
    Форматирует число для вывода, корректно подавляя артефакты округления.

    Args:
        num (float|int): Число для форматирования.

    Returns:
        str: Число в виде строки, без лишних нулей и ошибок округления.
    """
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
