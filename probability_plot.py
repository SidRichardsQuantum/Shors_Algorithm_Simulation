import numpy as np
import matplotlib.pyplot as plt
from quantum_part import run_shors_quantum_algorithm


def plot_first_register_probabilities(N, a, save_plot=False, filename=None):
    """
    Plot the first register probabilities.

    Args:
        N: Number to factor
        a: Base for the modular exponentiation
        save_plot: Whether to save the plot to file
        filename: Name of file to save (if save_plot=True)
    """
    # Run the quantum algorithm
    prob_first_register, M, _ = run_shors_quantum_algorithm(N, a)

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

    # Add probability values on bars
    for i, prob in enumerate(prob_first_register):
        if prob > 0.01:  # Only show labels for significant probabilities
            plt.text(i, prob + 0.01, f'{prob:.3f}', ha='center', va='bottom')

    plt.tight_layout()

    if save_plot and filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Plot saved as {filename}")

    plt.show()

    # Print analysis
    print(f"\n--- Shor's Algorithm Analysis ---")
    print(f"N = {N}, a = {a}")
    print(f"Function f(x) = {a}^x mod {N}:")
    for x in range(M):
        print(f"  f({x}) = {a}^{x} mod {N} = {pow(a, x, N)}")

    print(f"\nFirst register probabilities:")
    for x in range(M):
        print(f"  P(|{x}⟩) = {prob_first_register[x]:.4f}")

    # Find the most probable states
    max_prob_indices = np.where(prob_first_register == np.max(prob_first_register))[0]
    print(f"\nMost probable measurement outcomes: {max_prob_indices}")
    print(f"Maximum probability: {np.max(prob_first_register):.4f}")

    return prob_first_register


# if __name__ == "__main__":
#     # Example usage
#     N = 15
#
#     probabilities = plot_first_register_probabilities(N, a, save_plot=True,
#                                                       filename=f"shors_N{N}_a{a}.png")
