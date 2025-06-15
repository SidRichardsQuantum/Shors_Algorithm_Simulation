import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import numpy as np
import matplotlib.pyplot as plt
import time
from main import shors_simulation

# Set matplotlib backend for Codespaces
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend


def time_shor_simulation(N, a, sparse=True):
    """Time a single Shor's algorithm simulation."""
    start_time = time.time()

    try:
        shors_simulation(N=N, a=a, show_plots=False, sparse=True)  # Don't show probability plots
        end_time = time.time()
        return end_time - start_time

    except Exception as e:
        print(f"Error with N={N}, a={a}: {e}")
        return None


def run_runtime_analysis(repeats=3, sparse=True):
    """Run Shor's algorithm for different N values and plot runtimes."""

    # Test cases: (N, a) pairs
    # Choose a values that are coprime to N for non-trivial runs
    test_cases = [
        (15, 2),  # 3 * 5, 8 qubits
        (21, 2),  # 3 * 7, 10 qubits
        (35, 2),  # 5 * 7, 12 qubits
        (55, 2),  # 5 * 11, 12 qubits
        (77, 6),  # 7 * 11, 14 qubits
        (91, 5)  # 7 * 13, 14 qubits
    ]

    N_values = []
    runtimes = []
    std_deviations = []
    print("Measuring Code Runtimes")

    for N, a in test_cases:
        # Run multiple times and take average for more reliable results
        times = []
        num_runs = repeats  # Average over repeats

        for run in range(num_runs):
            runtime = time_shor_simulation(N, a, sparse)
            if runtime is not None:
                times.append(runtime)

        if times:
            avg_runtime = np.mean(times)
            std_runtime = np.std(times)

            N_values.append(N)
            runtimes.append(avg_runtime)
            std_deviations.append(std_runtime)

            print(f"N={N}: Avg: {avg_runtime:.4f}s (±{std_runtime:.4f}s)")
            print("=" * 40)

        else:
            print(f"N={N}: Failed")

    # Create the plot
    plt.figure(figsize=(12, 8))

    # Main runtime plot with error bars
    plt.subplot(2, 1, 1)
    plt.errorbar(N_values, runtimes, yerr=std_deviations,
                 fmt='bo-', linewidth=2, markersize=6,
                 capsize=5, capthick=2, elinewidth=2)
    plt.xlabel('N')
    plt.ylabel('Runtime (seconds)')
    plt.title("Shor's Algorithm Classical Simulation"
              "\nRuntime vs Semiprime")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save the plot instead of showing it
    output_file = f'images/shors_runtime_analysis_sparse_{sparse}_repeats_{repeats}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nPlot saved as: {output_file}")

    # plt.show()

    # Close the figure to free memory
    plt.close()

    return N_values, runtimes, std_deviations


if __name__ == "__main__":
    try:
        N_vals, times, stds = run_runtime_analysis(3, sparse=False)
        print("\nRuntime analysis complete!")

    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user.")

    except Exception as e:
        print(f"Error during analysis: {e}")
