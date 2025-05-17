from typing import Tuple, Dict

def calculate_expectation(uhu_dict: Dict[Tuple[int, ...], complex]) -> float:
    """
    Вычисляет среднее значение энергии ⟨0|U†HU|0⟩ для состояния |0...0⟩.

    Args:
        uhu_dict (Dict[Tuple[int, ...], complex]): Разложение оператора U†HU
            по базису Паули (ключ: индекс, значение: коэффициент).

    Returns:
        float: Ожидаемое значение (энергия).

    Примечание:
        - Только те операторы, которые не изменяют |0...0⟩ (то есть содержащие только I и Z),
          могут дать нетривиальный вклад в среднее значение.
    """
    expectation = 0.0
    for op, coeff in uhu_dict.items():
        if all(p in (0, 3) for p in op):  # Только I или Z на каждом кубите
            expectation += coeff.real
    return expectation
