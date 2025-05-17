def calculate_temp_steps(initial_temp: float, cooling_rate: float, min_temp: float) -> int:
    """
    Вычисляет количество температурных шагов для алгоритма отжига.

    Args:
        initial_temp (float): Начальная температура.
        cooling_rate (float): Коэффициент охлаждения.
        min_temp (float): Минимальная температура.

    Returns:
        int: Количество шагов снижения температуры.
    """
    steps = 0
    current_temp = initial_temp
    while current_temp > min_temp:
        current_temp *= cooling_rate
        steps += 1
    return steps
