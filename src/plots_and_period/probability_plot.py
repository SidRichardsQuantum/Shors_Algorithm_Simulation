import numpy as np
from math import log2, ceil
import matplotlib.pyplot as plt
from src.quantum_part.run_quantum_gates import run_quantum_gates


def plot_probs(N, a):
    """
    Plot the first register probabilities.

    Args:
        N: Number to factor
        a: Base for the modular exponentiation
    """

    n_qubits = ceil(log2(N))
    M = 2 ** n_qubits

    # Run the quantum algorithm
    phi = run_quantum_gates(N, a)

    # Extract the first register state probabilities
    # (A real implementation of Shor's algorithm would instead make a measurement of the first register.)
    prob_first_register = np.zeros(M)
    for x in range(M):
        for y in range(M):
            state_index = x * M + y
            prob_first_register[x] += np.abs(phi[state_index]) ** 2

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.bar(range(M), prob_first_register, alpha=0.7,
            color='lightcoral', edgecolor='darkred')
    plt.xlabel('First Register State |x⟩')
    plt.ylabel('Probability')
    plt.title(f'First Register Measurement Probabilities\n(Period detection for N={N}, a={a})')
    plt.grid(True, alpha=0.3)
    plt.xticks(range(M), [f'|{x}⟩' for x in range(M)])

    # # Add probability values on bars
    # for i, prob in enumerate(prob_first_register):
    #     if prob > 0.01:  # Only show labels for significant probabilities
    #         plt.text(i, prob + 0.01, f'{prob:.3f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

    return prob_first_register
