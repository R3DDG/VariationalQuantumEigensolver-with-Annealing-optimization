import numpy as np
from typing import Tuple, List, Dict
from .pauli_compose import pauli_compose

def compute_uhu(
    u_dict: Dict[Tuple[int, ...], complex], h_terms: List[Tuple[complex, List[int]]]
) -> Dict[Tuple[int, ...], complex]:
    """
    Вычисляет оператор U† H U.
    Возвращает: словарь {оператор: коэффициент}
    """
    uhu_dict = {}
    u_items = list(u_dict.items())
    for coeff_h, op_h in h_terms:
        op_h_tuple = tuple(op_h)
        for j_op, j_coeff in u_items:
            conj_j_coeff = np.conj(j_coeff)
            c1, op_uh = pauli_compose(j_op, op_h_tuple)
            for k_op, k_coeff in u_items:
                c2, op_uhu = pauli_compose(op_uh, k_op)
                total_coeff = conj_j_coeff * k_coeff * coeff_h * c1 * c2
                uhu_dict[op_uhu] = uhu_dict.get(op_uhu, 0) + total_coeff
    return uhu_dict
