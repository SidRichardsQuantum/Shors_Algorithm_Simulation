import numpy as np
from math import log2, ceil


def hadamard_matrix(n_qubits):
    """
    Create Hadamard operator for the first register only.

    This creates a superposition of all states in the first register,
    where all states have equal amplitude.
    """

    M = 2 ** n_qubits

    # Single qubit Hadamard
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

    # Multi-qubit Hadamard for first register
    H_first_register = H
    for i in range(n_qubits - 1):
        H_first_register = np.kron(H_first_register, H)

    # Identity for second register
    I_second_register = np.eye(M, dtype=complex)

    # Total Hadamard operation (H_0 ⊗ H_1 ⊗ ... H_{n_qubits - 1} ⊗ I_m)
    H_total_register = np.kron(H_first_register, I_second_register)

    return H_total_register
