from src.classical_parts.pre_checks import pre_checks
from src.plots_and_period.find_period import period
from src.classical_parts.post_checks import post_checks


def shors_simulation(N=15):
    """
    Shor's algorithm simulation.
    Default: N = 15

    Args:
        N: Integer to factor
    """

    # Classical preprocessing
    print(f"N = {N}\nRunning Classical Checks...")
    success, value, message = pre_checks(N)
    print(message)

    if success is True:
        # Classical checks found factors
        factors = value
        text = f"\nClassical methods found factors!\nNo quantum computation needed."
        return factors, text

    else:
        # Classical checks passed, proceed to the quantum part
        print(f"\nProceeding to quantum algorithm...")

        # Run quantum algorithm and plot probabilities
        a = value
        r = period(N, a)
        print(f"The period r is {r}")
        even, factors, text = post_checks(N, a, r)
        print(text)
