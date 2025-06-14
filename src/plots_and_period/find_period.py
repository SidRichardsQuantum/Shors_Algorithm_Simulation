import numpy as np
from src.plots_and_period.probability_plot import plot_probs

def period(N, a):
    """
    The period is the difference in index between adjacent states with the highest probabilities,
    so we find the most probable states.
    """

    prob_first_register = plot_probs(N, a)
    max_prob_indices = np.where(prob_first_register == np.max(prob_first_register))[0]
    print(f"\nMost probable measurement outcomes: {max_prob_indices}")
    r = max_prob_indices[1] - max_prob_indices[0]

    return r
