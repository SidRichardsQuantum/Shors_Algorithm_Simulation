import numpy as np
from scipy.sparse import csr_matrix, kron as sparse_kron, eye as sparse_eye


def iqft_first_register(M):
    """
    Create inverse QFT matrix for the first register.

    This matrix increases the amplitude size for states with index b * m / r,
    for non-negative integer b, and decreases all other state amplitude sizes.
    """

    iqft_first_register = np.zeros((M, M), dtype=complex)
    for k in range(M):
        for l in range(M):
            iqft_first_register[k, l] = (1 / np.sqrt(M)) * np.exp(2j * np.pi * k * l / M)

    return iqft_first_register


def iqft_matrix(M):
    """Create inverse QFT operator for the total register"""

    I_second_register = np.eye(M, dtype=complex)
    iqft_total_register = np.kron(iqft_first_register(M), I_second_register)

    return iqft_total_register


def iqft_first_register_sparse(M):
    """
    Create sparse inverse QFT matrix for the first register.

    This matrix increases the amplitude size for states with index b * m / r,
    for non-negative integer b, and decreases all other state amplitude sizes.
    """

    # Create arrays for row and column indices
    k_vals = np.arange(M)
    l_vals = np.arange(M)

    # Create meshgrid for all combinations
    K, L = np.meshgrid(k_vals, l_vals, indexing='ij')

    # Flatten to get 1D arrays
    k_flat = K.flatten()
    l_flat = L.flatten()

    # Compute the matrix elements (vectorized)
    # iqft_first_register[k, l] = (1 / sqrt(M)) * exp(2πi * k * l / M)
    factor = 1.0 / np.sqrt(M)
    phase = 2j * np.pi * k_flat * l_flat / M
    data = factor * np.exp(phase)

    # Create sparse matrix
    iqft_sparse = csr_matrix((data, (k_flat, l_flat)), shape=(M, M), dtype=complex)

    return iqft_sparse


def iqft_matrix_sparse(M):
    """Create sparse inverse QFT operator for the total register"""

    # Get sparse IQFT for first register
    iqft_first = iqft_first_register_sparse(M)

    # Sparse identity for second register
    I_second_register = sparse_eye(M, dtype=complex, format='csr')

    # Kronecker product of sparse matrices
    iqft_total_register = sparse_kron(iqft_first, I_second_register, format='csr')

    return iqft_total_register