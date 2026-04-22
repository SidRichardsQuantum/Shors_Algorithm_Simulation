from shors_algorithm_simulation import compute_probs, shors_simulation
from shors_algorithm_simulation.plotting.probabilities import plot_probs

if __name__ == "__main__":
    """Run a deterministic factorisation example with plot output."""
    result = shors_simulation(N=35, a=2, sparse=True, mode="distribution")
    probabilities = compute_probs(35, 2, sparse=True, mode="distribution")
    plot_probs(35, 2, probabilities, show_plots=True, output_dir="images")
    print(f"Structured result: factors={result['factors']}, period={result['period']}")
