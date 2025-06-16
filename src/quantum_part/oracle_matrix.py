import numpy as np
from math import log2, ceil
from scipy.sparse import csr_matrix


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


def oracle_matrix_sparse(N, a):
    """Even more efficient version using sparse matrices."""

    n_qubits = ceil(log2(N))
    M = 2 ** n_qubits
    total_size = M ** 2

    # Create arrays for all x and y values
    x_vals = np.arange(M)
    y_vals = np.arange(M)

    # Create meshgrid for all combinations
    X, Y = np.meshgrid(x_vals, y_vals, indexing='ij')

    # Flatten to get 1D arrays
    x_flat = X.flatten()
    y_flat = Y.flatten()

    # Compute input and output states
    input_states = x_flat * M + y_flat
    a_power_x = np.array([pow(a, int(x), N) for x in x_flat])
    output_y = (y_flat + a_power_x) % N
    output_states = x_flat * M + output_y

    # Create sparse matrix (more memory efficient)
    data = np.ones(total_size, dtype=complex)
    U_sparse = csr_matrix((data, (output_states, input_states)),
                          shape=(total_size, total_size))

    return U_sparse
