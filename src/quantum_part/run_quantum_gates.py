import numpy as np
from math import log2, ceil
from src.quantum_part.hadamard_matrix import hadamard_matrix_sparse, hadamard_matrix
from src.quantum_part.oracle_matrix import oracle_matrix_sparse, oracle_matrix
from src.quantum_part.iqft_matrix import iqft_matrix, iqft_matrix_sparse


def run_quantum_gates(N, a, sparse=True):
    """
    Run the quantum part of Shor's algorithm.

    First applies the Hadamard matrix, followed by the oracle matrix,
    then finally the inverse QFT matrix.

    Args:
        N: Semiprime to factorise
        a: Random integer base for modular exponentiation

    Returns:
        tuple: (prob_first_register, M, final_state)
    """

    n_qubits = ceil(log2(N))
    M = 2 ** n_qubits

    # Initialize state |0⟩|0⟩
    phi1 = np.zeros(M, dtype=complex)
    phi2 = np.zeros(M, dtype=complex)
    phi1[0] = 1.0
    phi2[0] = 1.0
    phi = np.kron(phi1, phi2)

    if sparse:  #Sparse matrices
        # Apply Hadamard matrix
        H = hadamard_matrix_sparse(n_qubits)
        phi = H @ phi

        # Apply oracle matrix
        U = oracle_matrix_sparse(N, a)
        phi = U @ phi

        # Apply inverse QFT matrix
        IQFT = iqft_matrix_sparse(M)
        phi = IQFT @ phi

    else:  # Dense matrices
        # Apply Hadamard matrix
        H = hadamard_matrix(n_qubits)
        phi = H @ phi

        # Apply oracle matrix
        U = oracle_matrix(N, a)
        phi = U @ phi

        # Apply inverse QFT matrix
        IQFT = iqft_matrix(M)
        phi = IQFT @ phi

    #Returns the final whole register state
    return phi
