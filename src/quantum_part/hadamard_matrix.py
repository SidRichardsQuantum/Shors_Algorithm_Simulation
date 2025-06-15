import numpy as np
from scipy.sparse import csr_matrix


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


def hadamard_matrix_sparse(n_qubits):
    """
    Efficient sparse matrix version of Hadamard operator for large n_qubits.
    
    Hadamard operation: |x⟩|y⟩ → (2^(-M/2)) Σ_z (-1)^(x·z) |z⟩|y⟩
    """

    M = 2 ** n_qubits
    total_size = M ** 2
    
    # Create arrays for all possible input states
    input_states = np.arange(total_size)
    
    # Extract x and y from input states: input_state = x * M + y
    x_vals = input_states // M
    y_vals = input_states % M
    
    # For each input state |x⟩|y⟩, we need M output states |z⟩|y⟩ for all z
    # Create arrays to store row indices, column indices, and data
    row_indices = []
    col_indices = []
    data_values = []
    
    normalization = 1.0 / np.sqrt(2 ** n_qubits)
    
    for input_idx in range(total_size):
        x = input_idx // M
        y = input_idx % M
        
        # For this input state |x⟩|y⟩, create superposition over all |z⟩|y⟩
        for z in range(M):
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
