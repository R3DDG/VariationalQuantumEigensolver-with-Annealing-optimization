def calculate_temp_steps(initial_temp: float, cooling_rate: float, min_temp: float) -> int:
    """
    Вычисляет количество температурных шагов для метода отжига.

    Алгоритм: на каждом шаге температура уменьшается по формуле:
        T_{n+1} = T_n * cooling_rate
    Шаги считаются, пока температура не станет меньше min_temp.

    Args:
        initial_temp (float): Начальная температура.
        cooling_rate (float): Множитель охлаждения (0 < cooling_rate < 1).
        min_temp (float): Минимально допустимая температура.

    Returns:
        int: Число температурных шагов до достижения min_temp.
    """
    steps = 0
    current_temp = initial_temp
    while current_temp > min_temp:
        current_temp *= cooling_rate
        steps += 1
    return steps
