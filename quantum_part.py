import numpy as np
from random import randint
from math import log2, ceil


def hadamard_first_register(m, n_qubits):
    """
    Create Hadamard operation on first register only.

    This creates a superposition of all states in the first register,
    where all states have equal amplitude.
    """
    # Single qubit Hadamard
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

    # Multi-qubit Hadamard for first register
    H_first = H
    for i in range(n_qubits - 1):
        H_first = np.kron(H_first, H)

    # Identity for second register
    I_second = np.eye(m, dtype=complex)

    # Total Hadamard operation (H⊗I)
    H_total = np.kron(H_first, I_second)

    return H_total


def oracle_unitary(m, a, N):
    """Create oracle function operator that maps |x⟩|y⟩ → |x⟩|(y + a^x) mod N⟩"""
    U = np.zeros((m * m, m * m), dtype=complex)

    for x in range(m):
        for y in range(m):
            input_state = x * m + y  # |x⟩|y⟩
            output_y = (y + pow(a, x, N)) % N
            output_state = x * m + output_y  # |x⟩|(y + a ** x) % N⟩
            U[output_state, input_state] = 1.0

    return U


def inverse_qft(m):
    """Create inverse QFT matrix"""
    IQFT = np.zeros((m, m), dtype=complex)

    for k in range(m):
        for l in range(m):
            IQFT[k, l] = (1 / np.sqrt(m)) * np.exp(2j * np.pi * k * l / m)

    return IQFT


def inverse_qft_first_register(m):
    """Create inverse QFT operation on first register only"""
    IQFT_first = inverse_qft(m)
    I_second = np.eye(m, dtype=complex)
    IQFT_total = np.kron(IQFT_first, I_second)
    return IQFT_total


def run_shors_quantum_algorithm(N, a):
    """
    Run the quantum part of Shor's algorithm.

    Args:
        N: Number to factor
        a: Base for the modular exponentiation

    Returns:
        tuple: (prob_first_register, M, final_state)
    """
    n_qubits = ceil(log2(N))
    M = 2 ** n_qubits

    # Initialize state |0⟩|0⟩
    phi = np.zeros(M * M, dtype=complex)
    phi[0] = 1.0

    # Apply Hadamard to first register only
    H_total = hadamard_first_register(M, n_qubits)
    phi = H_total @ phi

    # Apply oracle U_f
    U = oracle_unitary(M, a, N)
    phi = U @ phi

    # Apply inverse QFT to first register only
    IQFT_total = inverse_qft_first_register(M)
    phi = IQFT_total @ phi

    # Extract measurement probabilities for first register
    prob_first_register = np.zeros(M)
    for x in range(M):
        for y in range(M):
            state_index = x * M + y
            prob_first_register[x] += np.abs(phi[state_index]) ** 2

    return prob_first_register, M, phi


# if __name__ == "__main__":
#     # Example usage
#     N = 15
#     a = randint(2, N)
#
#     prob_first_register, M, final_state = run_shors_quantum_algorithm(N, a)
#
#     print(f"N = {N}, a = {a}")
#     print(f"Function f(x) = {a}^x mod {N}:")
#     for x in range(M):
#         print(f"  f({x}) = {a}^{x} mod {N} = {pow(a, x, N)}")
#
#     print(f"\nFirst register probabilities:")
#     for x in range(M):
#         print(f"  P(|{x}⟩) = {prob_first_register[x]:.4f}")
