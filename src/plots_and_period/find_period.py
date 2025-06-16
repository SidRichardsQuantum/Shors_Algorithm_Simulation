import numpy as np
from math import log2, ceil
from src.plots_and_period.probability_plot import compute_probs


def find_period(N, a, sparse=True):
    """
    The period is the difference in index between adjacent states with probabilities above the mean.
    """

    n_qubits = ceil(log2(N))
    M = 2 ** n_qubits
    
    # Calculate mean probability
    prob_first_register = compute_probs(N, a, sparse)  # Just compute, don't plot
    mean_prob = np.mean(prob_first_register)
    
    # Find indices where probability is above the mean
    above_mean_indices = np.where(prob_first_register >= mean_prob)[0]

    # Use the differences between above-mean states to estimate period candidates
    s = []  # Period candidates list
    for i in range(1, len(above_mean_indices)):
        s.append(M * i / (above_mean_indices[i] - above_mean_indices[0]))
    r = round(np.mean(s))  # Average of the candidates, as an integer
    
    return r, prob_first_register  # Return both period and probabilities
