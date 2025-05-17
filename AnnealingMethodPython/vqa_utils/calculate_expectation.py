from typing import Tuple, Dict

def calculate_expectation(uhu_dict: Dict[Tuple[int, ...], complex]) -> float:
    """
    Вычисляет ⟨0|U†HU|0⟩ для состояния |0...0⟩.
    Возвращает: ожидаемое значение
    """
    expectation = 0.0
    for op, coeff in uhu_dict.items():
        if all(p in (0, 3) for p in op):  # I или Z
            expectation += coeff.real
    return expectation
