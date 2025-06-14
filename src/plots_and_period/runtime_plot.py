import time
import matplotlib.pyplot as plt
import numpy as np
from main import shors_simulation


def time_shor_simulation(N, a):
    """Time a single Shor's algorithm simulation."""
    start_time = time.time()
    try:
        shors_simulation(N=N, a=a, show_plots=False)  # Don't show plots
        end_time = time.time()
        return end_time - start_time
    except Exception as e:
        print(f"Error with N={N}, a={a}: {e}")
        return None


def run_runtime_analysis():
    """Run Shor's algorithm for different N values and plot runtimes."""

    # Test cases: (N, a) pairs
    # Choose a values that are coprime to N for non-trivial Shor's algorithm runs
    test_cases = [
        (15, 7),  # 3 * 5 default example
        (21, 8),  # 3 * 7
        (33, 10),  # 3 * 11
        (35, 6),  # 5 * 7
        (51, 8),  # 3 * 17
        (55, 7),  # 5 * 11
        # (77, 8),   # 7 * 11
        # (91, 6),   # 7 * 13
        # (95, 3),   # 5 * 19
        # (115, 3),  # 5 * 23
        # (143, 5),  # 8 qubits
        # (209, 6),  # 8 qubits
        # (253, 7),  # 8 qubits
        # (323, 5),  # 9 qubits (17×19)
        # (391, 6),  # 9 qubits (17×23)
    ]

    N_values = []
    runtimes = []

    # print("Running Shor's Algorithm Simulation"
    #       "\n Measuring Code Runtimes")

    for N, a in test_cases:
        # Run multiple times and take average for more reliable results
        times = []
        num_runs = 1  # Average over 3 repeats

        for run in range(num_runs):
            runtime = time_shor_simulation(N, a)
            if runtime is not None:
                times.append(runtime)

        if times:
            avg_runtime = np.mean(times)
#            std_runtime = np.std(times)

            N_values.append(N)
            runtimes.append(avg_runtime)

#            print(f"Avg: {avg_runtime:.4f}s (±{std_runtime:.4f}s)")
            print("-" * 40)
        else:
            print("Failed")

    # Create the plot
    plt.figure(figsize=(12, 8))

    # Main runtime plot
    plt.subplot(2, 1, 1)
    plt.plot(N_values, runtimes, 'bo-', linewidth=2, markersize=8)
    plt.xlabel('N')
    plt.ylabel('Runtime (seconds)')
    plt.title("Shor's Algorithm Runtime vs Semiprime size")
    plt.grid(True, alpha=0.3)

    # for i, (n, t) in enumerate(zip(N_values, runtimes)):
    #     plt.annotate(f'{t:.3f}s', (n, t), textcoords="offset points",
    #                  xytext=(0, 10), ha='center', fontsize=9)

    plt.tight_layout()
    plt.show()

    return N_values, runtimes


if __name__ == "__main__":
    try:
        run_runtime_analysis()
        print("\nRuntime analysis complete!")

    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user.")
    except Exception as e:
        print(f"Error during analysis: {e}")
