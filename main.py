from src.classical_parts.pre_checks import pre_checks
from src.plots_and_period.find_period import find_period
from src.classical_parts.post_checks import post_checks
from src.plots_and_period.probability_plot import plot_probs


def shors_simulation(N=15, a=None, show_plots=True, sparse=True):
    """
    Shor's algorithm simulation.
    Default: N = 15

    Args:
        N: Integer to factor
        a: Base for modular exponentiation. If None, will be chosen randomly.
           Must be between 2 and N-1 (inclusive).
    """

    # Validate a if provided
    if a is not None:
        if not (2 <= a <= N - 1):
            raise ValueError(f"Invalid value for 'a': {a}. Must be between 2 and {N - 1} (inclusive).")

    # Classical preprocessing
    print(f"N = {N}\nRunning Classical Checks...")
    success, value, message = pre_checks(N, a)
    print(message)

    if success is True:
        # Classical checks found factors
        factors = value
        text = f"\nClassical methods found factors!\nNo quantum computation needed."
        return factors, text

    else:
        # Classical checks passed, proceed to the quantum part
        print("Proceeding to quantum algorithm...")

        # 'value' from pre_checks is now the 'a' that was used
        a = value

        # Run the algorithm
        r, probabilities = find_period(N, a, sparse)

        # Do the factorization
        result = post_checks(N, a, r)
        print(result)

        # Now show the plot
        plot_probs(N, a, probabilities, show_plots=show_plots, sparse=sparse)
    
