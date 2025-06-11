#import numpy as np
import matplotlib.pyplot as plt
from src.quantum_part.quantum_part import run_quantum_gates


def plot_first_register_probabilities(N, a):
    """
    Plot the first register probabilities.

    Args:
        N: Number to factor
        a: Base for the modular exponentiation
    """

    # Run the quantum algorithm
    prob_first_register, M, _ = run_quantum_gates(N, a)

    # Create the plot
    plt.figure(figsize=(10, 6))
    first_reg_states = range(M)
    plt.bar(first_reg_states, prob_first_register, alpha=0.7,
            color='lightcoral', edgecolor='darkred')
    plt.xlabel('First Register State |x⟩')
    plt.ylabel('Probability')
    plt.title(f'First Register Measurement Probabilities\n(Period detection for N={N}, a={a})')
    plt.grid(True, alpha=0.3)
    plt.xticks(first_reg_states, [f'|{x}⟩' for x in range(M)])

    # # Add probability values on bars
    # for i, prob in enumerate(prob_first_register):
    #     if prob > 0.01:  # Only show labels for significant probabilities
    #         plt.text(i, prob + 0.01, f'{prob:.3f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

    # Print analysis
    print(f"\n--- Shor's Algorithm Analysis ---")
    print(f"N = {N}, a = {a}")

    # # Find the most probable states
    # max_prob_indices = np.where(prob_first_register == np.max(prob_first_register))[0]
    # print(f"\nMost probable measurement outcomes: {max_prob_indices}")
    # print(f"Maximum probability: {np.max(prob_first_register):.4f}")

    return prob_first_register
