import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import shors_simulation


if __name__ == "__main__":
    """Run multiple semiprime examples with fixed bases for quick experimentation."""
    cases = [
        (15, 2, "distribution"),
        (21, 2, "distribution"),
        (33, 5, "distribution"),
        (15, 2, "matrix"),
    ]

    for N, a, mode in cases:
        print("\n" + "=" * 60)
        print(f"Running example with N={N}, a={a}, mode={mode}")
        print("=" * 60)
        result = shors_simulation(N=N, a=a, show_plots=False, sparse=True, mode=mode)
        print(f"Structured result: success={result['success']}, factors={result['factors']}, period={result['period']}")

    print("\n" + "=" * 60)
    print("Expected retry case with N=33, a=2")
    print("=" * 60)
    result = shors_simulation(N=33, a=2, show_plots=False, sparse=True, mode="distribution")
    print(f"Structured result: success={result['success']}, message={result['message']}")
