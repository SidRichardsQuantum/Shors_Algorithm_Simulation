import time
import matplotlib.pyplot as plt
import numpy as np
from main import shors_simulation


def time_shor_simulation(N, a):
    """Time a single Shor's algorithm simulation."""
    start_time = time.time()

    try:
        shors_simulation(N=N, a=a, show_plots=False, sparse=True)  # Don't show probability plots
        end_time = time.time()
        return end_time - start_time

    except Exception as e:
        print(f"Error with N={N}, a={a}: {e}")
        return None


def run_runtime_analysis(repeats=3):
    """Run Shor's algorithm for different N values and plot runtimes."""

    # Test cases: (N, a) pairs
    # Choose a values that are coprime to N for non-trivial Shor's algorithm runs
    test_cases = [
        (15, 7),  # 3 * 5, period = 4
        # (21, 8),  # 3 * 7, period = 2
        # (33, 10),  # 3 * 11, period = 10
        # (35, 6),  # 5 * 7, period = 4
        (51, 8),  # 3 * 17, period = 8
        # (55, 7),  # 5 * 11, period = 10
        # (77, 8),  # 7 * 11, period = 10
        # (91, 6),  # 7 * 13, period = 12
        # (95, 3),  # 5 * 19, period = 18
        (115, 2),  # 5 * 23, try a=2 (period likely smaller than a=3)
        # (143, 2),  # 11 * 13, a=2 should give smaller period than a=5
        (209, 2),  # 11 * 19, a=2 typically has smaller periods
        (253, 2),  # 11 * 23, a=2 should be better than a=7
        # (323, 2),  # 17 * 19, a=2 should work better than a=5
        # (391, 2),  # 17 * 23, a=2 likely better than a=6
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
            runtime = time_shor_simulation(N, a)
            if runtime is not None:
                times.append(runtime)

        if times:
            avg_runtime = np.mean(times)
            std_runtime = np.std(times)

            N_values.append(N)
            runtimes.append(avg_runtime)
            std_deviations.append(std_runtime)

            print(f"N={N}: Avg: {avg_runtime:.4f}s (±{std_runtime:.4f}s)")
            print("-" * 40)

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
    plt.show()

    return N_values, runtimes, std_deviations


if __name__ == "__main__":
    try:
        N_vals, times, stds = run_runtime_analysis(1)
        print("\nRuntime analysis complete!")

    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user.")

    except Exception as e:
        print(f"Error during analysis: {e}")
