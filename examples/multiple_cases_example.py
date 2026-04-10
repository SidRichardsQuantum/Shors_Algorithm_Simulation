import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import shors_simulation


if __name__ == "__main__":
    """Run multiple semiprime examples with fixed bases for quick experimentation."""
    cases = [
        (15, 2),
        (21, 2),
        (33, 2),
    ]

    for N, a in cases:
        print("\n" + "=" * 60)
        print(f"Running example with N={N}, a={a}")
        print("=" * 60)
        shors_simulation(N=N, a=a, show_plots=False, sparse=True)
