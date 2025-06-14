import numpy as np
from math import log2, ceil


def oracle_matrix(N, a):
    """
    Create unitary oracle operator that maps |x⟩|y⟩ → |x⟩|(y + a^x) mod N⟩.

    This entangles the registers and encodes periodicity.
    """

    n_qubits = ceil(log2(N))
    M = 2 ** n_qubits
    U = np.zeros((M ** 2, M ** 2), dtype=complex)
    for x in range(M):
        for y in range(M):
            input_state = x * M + y  # |x⟩|y⟩
            output_y = (y + pow(a, x, N)) % N
            output_state = x * M + output_y  # |x⟩|(y + a^x) mod N⟩
            U[output_state, input_state] = 1.0

    return U
