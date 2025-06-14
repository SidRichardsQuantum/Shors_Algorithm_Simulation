import numpy as np
from math import log2, ceil
from src.plots_and_period.probability_plot import compute_probs


def find_period(N, a, sparse=True):
    """
    The period is the difference in index between adjacent states with the highest probabilities.
    """
    n_qubits = ceil(log2(N))
    M = 2 ** n_qubits

    prob_first_register = compute_probs(N, a, sparse=True)  # Just compute, don't plot
    max_prob_indices = np.where(prob_first_register == np.max(prob_first_register))[0]
    print(f"\nMost probable measurement outcomes: {max_prob_indices}")
    r = int(M / (max_prob_indices[1] - max_prob_indices[0]))

    return r, prob_first_register  # Return both period and probabilities
