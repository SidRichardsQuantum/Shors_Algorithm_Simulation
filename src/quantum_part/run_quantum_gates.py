import numpy as np
from math import log2, ceil
from src.quantum_part.hadamard_matrix import hadamard_matrix_sparse, hadamard_matrix
from src.quantum_part.oracle_matrix import oracle_matrix_sparse, oracle_matrix
from src.quantum_part.iqft_matrix import iqft_matrix, iqft_matrix_sparse


def run_quantum_gates(N, a, sparse=True, first_register_qubits=None, second_register_qubits=None):
    """
    Run the quantum part of Shor's algorithm.

    First applies the Hadamard matrix, followed by the oracle matrix,
    then finally the inverse QFT matrix.

    Args:
        N: Semiprime to factorise
        a: Random integer base for modular exponentiation
        first_register_qubits: Number of qubits in the period register.
        second_register_qubits: Number of qubits in the function register.

    Returns:
        tuple: (prob_first_register, M, final_state)
    """

    n_qubits = ceil(log2(N))
    if first_register_qubits is None:
        first_register_qubits = 2 * n_qubits
    if second_register_qubits is None:
        second_register_qubits = n_qubits

    Q = 2 ** first_register_qubits
    M = 2 ** n_qubits
    if M != 2 ** second_register_qubits:
        M = 2 ** second_register_qubits

    total_size = Q * M
    max_sparse_hadamard_entries = 5_000_000
    max_dense_states = 2048

    if sparse and total_size * Q > max_sparse_hadamard_entries:
        raise MemoryError(
            f"Matrix mode would create {total_size * Q:,} Hadamard entries. "
            "Use mode='distribution' for this input."
        )
    if not sparse and total_size > max_dense_states:
        raise MemoryError(
            f"Dense matrix mode would create {total_size:,} x {total_size:,} matrices. "
            "Use sparse=True or mode='distribution'."
        )

    # Initialize state |0⟩|0⟩
    phi1 = np.zeros(Q, dtype=complex)
    phi2 = np.zeros(M, dtype=complex)
    phi1[0] = 1.0
    phi2[0] = 1.0
    phi = np.kron(phi1, phi2)

    if sparse:  #Sparse matrices
        # Apply Hadamard matrix
        H = hadamard_matrix_sparse(first_register_qubits, second_register_qubits)
        phi = H @ phi

        # Apply oracle matrix
        U = oracle_matrix_sparse(N, a, first_register_qubits, second_register_qubits)
        phi = U @ phi

        # Apply inverse QFT matrix
        IQFT = iqft_matrix_sparse(Q, M)
        phi = IQFT @ phi

    else:  # Dense matrices
        # Apply Hadamard matrix
        H = hadamard_matrix(first_register_qubits, second_register_qubits)
        phi = H @ phi

        # Apply oracle matrix
        U = oracle_matrix(N, a, first_register_qubits, second_register_qubits)
        phi = U @ phi

        # Apply inverse QFT matrix
        IQFT = iqft_matrix(Q, M)
        phi = IQFT @ phi

    #Returns the final whole register state
    return phi
