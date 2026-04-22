import numpy as np
from math import log2, ceil
from scipy.sparse import csr_matrix


def oracle_matrix(N, a, first_register_qubits=None, second_register_qubits=None):
    """
    Create a unitary oracle that maps |x⟩|y⟩ → |x⟩|y xor a^x mod N⟩.

    This entangles the registers and encodes periodicity.
    """

    n_qubits = ceil(log2(N))
    if first_register_qubits is None:
        first_register_qubits = n_qubits
    if second_register_qubits is None:
        second_register_qubits = n_qubits

    Q = 2**first_register_qubits
    M = 2**second_register_qubits
    total_size = Q * M

    U = np.zeros((total_size, total_size), dtype=complex)
    for x in range(Q):
        for y in range(M):
            input_state = x * M + y  # |x⟩|y⟩
            output_y = y ^ pow(a, x, N)
            output_state = x * M + output_y  # |x⟩|y xor a^x mod N⟩
            U[output_state, input_state] = 1.0

    return U


def oracle_matrix_sparse(N, a, first_register_qubits=None, second_register_qubits=None):
    """Even more efficient version using sparse matrices."""

    n_qubits = ceil(log2(N))
    if first_register_qubits is None:
        first_register_qubits = n_qubits
    if second_register_qubits is None:
        second_register_qubits = n_qubits

    Q = 2**first_register_qubits
    M = 2**second_register_qubits
    total_size = Q * M

    # Create arrays for all x and y values
    x_vals = np.arange(Q)
    y_vals = np.arange(M)

    # Create meshgrid for all combinations
    X, Y = np.meshgrid(x_vals, y_vals, indexing="ij")

    # Flatten to get 1D arrays
    x_flat = X.flatten()
    y_flat = Y.flatten()

    # Compute input and output states
    input_states = x_flat * M + y_flat
    a_power_x = np.array([pow(a, int(x), N) for x in x_flat])
    output_y = y_flat ^ a_power_x
    output_states = x_flat * M + output_y

    # Create sparse matrix (more memory efficient)
    data = np.ones(total_size, dtype=complex)
    U_sparse = csr_matrix(
        (data, (output_states, input_states)), shape=(total_size, total_size)
    )

    return U_sparse
