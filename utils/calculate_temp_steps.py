def calculate_temp_steps(initial_temp: float, cooling_rate: float, min_temp: float) -> int:
    steps = 0
    current_temp = initial_temp
    while current_temp > min_temp:
        current_temp *= cooling_rate
        steps += 1

    return steps
