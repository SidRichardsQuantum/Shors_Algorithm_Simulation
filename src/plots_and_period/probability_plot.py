import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import numpy as np
from math import log2, ceil
from src.plots_and_period.plot_formatting import set_ket_xticks
from src.quantum_part.run_quantum_gates import run_quantum_gates

# Set matplotlib backend for Codespaces
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt


def compute_probs(N, a, sparse=True, mode="distribution"):
    """
    Compute the first register probabilities without plotting.

    Both modes use Q ~= N^2 first-register states, which is the usual Shor
    period-finding scale. Matrix mode builds and applies the gates directly;
    distribution mode computes the same ideal first-register distribution
    without materializing the full matrices.
    """
    n_qubits = ceil(log2(N))
    Q = 2 ** (2 * n_qubits)
    M = 2 ** n_qubits

    if mode == "matrix":
        phi = run_quantum_gates(
            N,
            a,
            sparse=sparse,
            first_register_qubits=2 * n_qubits,
            second_register_qubits=n_qubits,
        )
        return np.sum(np.abs(phi.reshape(Q, M)) ** 2, axis=1)

    if mode != "distribution":
        raise ValueError("mode must be 'distribution' or 'matrix'")

    oracle_values = np.empty(Q, dtype=int)
    value = 1
    for x in range(Q):
        oracle_values[x] = value
        value = (value * a) % N

    prob_first_register = np.zeros(Q)
    for y in np.unique(oracle_values):
        indicator = (oracle_values == y).astype(float)
        amplitudes = np.fft.ifft(indicator)
        prob_first_register += np.abs(amplitudes) ** 2

    return prob_first_register


def plot_probs(N, a, prob_first_register, show_plots=True, sparse=True):
    """
    Plot the probabilities that were already computed.
    """
    Q = len(prob_first_register)
    tick_step = max(1, Q // 16)

    plt.figure(figsize=(10, 6))
    plt.bar(range(Q), prob_first_register, alpha=0.7,
            color='lightcoral', edgecolor='darkred')
    plt.xlabel('First Register State')
    plt.ylabel('Probability')
    plt.title(f'First Register Measurement Probabilities\n(Period detection for N={N}, a={a})')
    plt.grid(True, alpha=0.3)
    axis = plt.gca()
    set_ket_xticks(axis, range(0, Q, tick_step))
    plt.tight_layout()
    print('-' * 40)

    if show_plots:
        # plt.show()  # Only show if requested

        # Save the plot instead of showing it
        output_file = f'images/first_register_probabilities_N={N}_a={a}.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"\nPlot saved as: {output_file}")

        # Close the figure to free memory
        plt.close()
    
    else:
        plt.close()
