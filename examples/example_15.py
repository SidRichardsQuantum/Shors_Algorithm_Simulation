from src.classical_parts.pre_checks import pre_checks
from src.plotters.probability_plot import plot_first_register_probabilities


def run_shors_demo(N=15):
    """
    Shor's algorithm simulation.
    Default: N = 15

    Args:
        N: Integer to factor
    """

    # Classical preprocessing
    print(f"N = {N}\nRunning Classical Checks...")

    success, result, message = pre_checks(N)
    print(message)

    if success:
        # Classical checks found factors
        factors = result
        print(f"\nClassical methods found factors!\nNo quantum computation needed.")
        return factors

    else:
        # Classical checks passed, proceed to quantum
        a = result
        print(f"\nProceeding to quantum algorithm...")

        try:
            # Run quantum algorithm and plot probabilities
            probabilities = plot_first_register_probabilities(N, a)
            return None

        except Exception as e:
            print(f"Error in quantum computation. Try again.")
            return None


if __name__ == "__main__":
    N = 21
    result = run_shors_demo(N=N)

    if result:
        print(f"\nClassical methods succeeded: {N} = {result[0]} × {result[1]}")
