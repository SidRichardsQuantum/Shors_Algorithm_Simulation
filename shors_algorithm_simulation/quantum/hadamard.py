import numpy as np
from scipy.sparse import csr_matrix


def hadamard_matrix(first_register_qubits, second_register_qubits=None):
    """
    Create Hadamard operator for the first register only.

    This creates a superposition of all states in the first register,
    where all states have equal amplitude.
    """

    if second_register_qubits is None:
        second_register_qubits = first_register_qubits

    Q = 2 ** first_register_qubits
    M = 2 ** second_register_qubits

    # Single qubit Hadamard
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

    # Multi-qubit Hadamard for first register
    H_first_register = H
    for i in range(first_register_qubits - 1):
        H_first_register = np.kron(H_first_register, H)

    # Identity for second register
    I_second_register = np.eye(M, dtype=complex)

    # Total Hadamard operation (H_0 ⊗ H_1 ⊗ ... H_{n_qubits - 1} ⊗ I_m)
    H_total_register = np.kron(H_first_register, I_second_register)

    return H_total_register


def hadamard_matrix_sparse(first_register_qubits, second_register_qubits=None):
    """
    Efficient sparse matrix version of Hadamard operator.
    
    Hadamard operation: |x⟩|y⟩ → (2^(-n/2)) Σ_z (-1)^(x·z) |z⟩|y⟩
    """

    if second_register_qubits is None:
        second_register_qubits = first_register_qubits

    Q = 2 ** first_register_qubits
    M = 2 ** second_register_qubits
    total_size = Q * M
    
    # For each input state |x⟩|y⟩, we need M output states |z⟩|y⟩ for all z
    # Create arrays to store row indices, column indices, and data
    row_indices = []
    col_indices = []
    data_values = []
    
    normalization = 1.0 / np.sqrt(Q)
    
    for input_idx in range(total_size):
        x = input_idx // M
        y = input_idx % M
        
        # For this input state |x⟩|y⟩, create superposition over all |z⟩|y⟩
        for z in range(Q):
            output_idx = z * M + y
            
            # Compute phase factor (-1)^(x·z) where · is bitwise dot product
            phase = (-1) ** bin(x & z).count('1')
            amplitude = normalization * phase
            
            row_indices.append(output_idx)
            col_indices.append(input_idx)
            data_values.append(amplitude)
    
    # Convert to numpy arrays
    row_indices = np.array(row_indices)
    col_indices = np.array(col_indices)
    data_values = np.array(data_values, dtype=complex)
    
    # Create sparse matrix
    H_sparse = csr_matrix((data_values, (row_indices, col_indices)),
                          shape=(total_size, total_size))
    
    return H_sparse
