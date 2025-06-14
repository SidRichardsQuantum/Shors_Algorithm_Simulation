import numpy as np
from math import log2, ceil
import matplotlib.pyplot as plt
from src.quantum_part.run_quantum_gates import run_quantum_gates


def compute_probs(N, a):
    """
    Compute the first register probabilities without plotting.
    """
    n_qubits = ceil(log2(N))
    M = 2 ** n_qubits

    # Run the quantum algorithm
    phi = run_quantum_gates(N, a)

    # Extract the first register state probabilities
    prob_first_register = np.zeros(M)
    for x in range(M):
        for y in range(M):
            state_index = x * M + y
            prob_first_register[x] += np.abs(phi[state_index]) ** 2

    return prob_first_register

def plot_probs(N, a, prob_first_register, show_plots=True):
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
    plt.xticks(range(M), [f'|{x}⟩' for x in range(M)])
    plt.tight_layout()

    if show_plots:
        plt.show()  # Only show if requested
    else:
        plt.close()
