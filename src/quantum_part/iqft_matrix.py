import numpy as np


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
