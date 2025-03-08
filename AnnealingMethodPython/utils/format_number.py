def format_number(num: float | int) -> str:
    """
    Универсальный форматировщик чисел с точным определением целочисленных значений
    и подавлением артефактов вычислений с плавающей точкой.
    """
    # Проверка на целое число с учетом погрешности вычислений
    if abs(num - round(num)) < 1e-12:
        return str(int(round(num)))

    # Форматирование с ручным управлением десятичными знаками
    s = f"{num:.14f}".rstrip("0").rstrip(".")

    # Исправление артефактов вида ".5" → "0.5"
    if s.startswith("."):
        s = "0" + s
    elif s.startswith("-."):
        s = s.replace("-.", "-0.")

    # Удаление лишних десятичных знаков после 4-го
    if "." in s:
        int_part, dec_part = s.split(".")
        dec_part = dec_part[:4].ljust(4, "0").rstrip("0")
        s = f"{int_part}.{dec_part}" if dec_part else int_part

    return s
