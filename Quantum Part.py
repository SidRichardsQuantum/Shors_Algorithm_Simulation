import numpy as np
from random import randint
from math import log2, ceil

N = 4
n_qubits = ceil(log2(N))
M = 2 ** n_qubits
a = randint(2, N)
print(f"a = {a}")


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


# Initialize state |0⟩|0⟩
phi = np.zeros(M * M, dtype=complex)  # (M^2)-dimensional state vector
phi[0] = 1.0

# Apply Hadamard to first register only
H_total = hadamard_first_register(M, n_qubits)
phi = H_total @ phi
print("After Hadamard:", phi)

# Apply oracle U_f
U = oracle_unitary(M, a, N)
phi = U @ phi
print("After oracle:", phi)

# Apply inverse QFT to first register only
IQFT_total = inverse_qft_first_register(M)
phi = IQFT_total @ phi
print("Final state:", phi)
print("Probabilities:", np.abs(phi) ** 2)

# To extract measurement probabilities for first register:
prob_first_register = np.zeros(M)
for x in range(M):
    for y in range(M):
        state_index = x * M + y
        prob_first_register[x] += np.abs(phi[state_index]) ** 2

print("First register probabilities:", prob_first_register)
