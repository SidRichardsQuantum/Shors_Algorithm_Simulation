import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import shors_simulation


if __name__ == "__main__":
    """Run a deterministic example without opening plots."""
    result = shors_simulation(N=21, a=2, show_plots=False, sparse=True, mode="distribution")
    print(f"Structured result: factors={result['factors']}, period={result['period']}")
