import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import numpy as np
import matplotlib.pyplot as plt
from math import log2, ceil
from src.quantum_part.run_quantum_gates import run_quantum_gates

# Set matplotlib backend for Codespaces
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend


def compute_probs(N, a, sparse=True):
    """
    Compute the first register probabilities without plotting.
    """
    n_qubits = ceil(log2(N))
    M = 2 ** n_qubits

    # Run the quantum algorithm
    phi = run_quantum_gates(N, a, sparse)

    # Extract the first register state probabilities
    prob_first_register = np.zeros(M)
    for x in range(M):
        for y in range(M):
            state_index = x * M + y
            prob_first_register[x] += np.abs(phi[state_index]) ** 2

    return prob_first_register

def plot_probs(N, a, prob_first_register, show_plots=True, sparse=True):
    """
    Plot the probabilities that were already computed.
    """
    n_qubits = ceil(log2(N))
    M = 2 ** n_qubits

    plt.figure(figsize=(10, 6))
    plt.bar(range(M), prob_first_register, alpha=0.7,
            color='lightcoral', edgecolor='darkred')
    plt.xlabel('First Register State |x⟩')
    plt.ylabel('Probability')
    plt.title(f'First Register Measurement Probabilities\n(Period detection for N={N}, a={a})')
    plt.grid(True, alpha=0.3)
    plt.xticks(range(0, M, n_qubits // 2), [f'|{x}⟩' for x in range(0, M, n_qubits // 2)])
    plt.tight_layout()
    print('-' * 40)

    if show_plots:
        # plt.show()  # Only show if requested

        # Save the plot instead of showing it
        output_file = f'images/first_register_probabilities_sparse_{sparse}.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"\nPlot saved as: {output_file}")

        # Close the figure to free memory
        plt.close()
    
    else:
        plt.close()
