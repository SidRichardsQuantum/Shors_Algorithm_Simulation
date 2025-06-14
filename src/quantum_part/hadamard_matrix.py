import numpy as np


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


# More efficient construction using properties of Kronecker products
def hadamard_matrix_efficient(n_qubits):
    """
    More efficient construction using the fact that H^⊗n has a known structure.
    The n-qubit Hadamard matrix can be constructed more efficiently.
    H^⊗n has entries: H[i,j] = (-1)^(i·j) / sqrt(2^n),
    where i·j is the bitwise dot product.
    """

    def bitwise_dot_product(a, b, n_bits):
        """Compute bitwise dot product of two integers"""
        return bin(a & b).count('1') % 2

    # Create the first register Hadamard matrix efficiently
    M = 2 ** n_qubits
    H_first = np.zeros((M, M), dtype=complex)
    factor = 1.0 / np.sqrt(M)

    for i in range(M):
        for j in range(M):
            H_first[i, j] = (-1) ** bitwise_dot_product(i, j, n_qubits) * factor

    # Identity for second register
    I_second = np.eye(M, dtype=complex)

    # Total Hadamard operation
    H_total = np.kron(H_first, I_second)

    return H_total
