from __future__ import annotations

import os

import numpy as np
from math import log2, ceil
import time
import csv
from shors_algorithm_simulation.core import shors_simulation
from shors_algorithm_simulation.plotting.matplotlib_helpers import get_pyplot


def timer(
    N: int, a: int, sparse: bool = True, mode: str = "distribution"
) -> float | None:
    """Time a single Shor's algorithm simulation."""
    start_time = time.time()
    try:
        shors_simulation(N=N, a=a, sparse=sparse, mode=mode)
        end_time = time.time()
        return end_time - start_time
    except Exception as e:
        print(f"Error with N={N}, a={a}: {e}")
        return None


def benchmark_runtime_table(
    test_cases: list[tuple[int, int]],
    repeats: int = 3,
    sparse: bool = True,
    output_csv: str = "images/runtime_benchmark.csv",
    mode: str = "distribution",
) -> list[dict[str, object]]:
    """
    Benchmark Shor's simulation and save tabular results to CSV.

    Each row contains:
    N, a, qubits, repeats, successes, mean_seconds, std_seconds, min_seconds, max_seconds, sparse, mode
    """

    rows = []
    print("Running runtime benchmark table...")
    for N, a in test_cases:
        times = []
        for _ in range(repeats):
            runtime = timer(N, a, sparse=sparse, mode=mode)
            if runtime is not None:
                times.append(runtime)

        total_qubits = 3 * ceil(log2(N))
        if times:
            row = {
                "N": N,
                "a": a,
                "qubits": total_qubits,
                "repeats": repeats,
                "successes": len(times),
                "mean_seconds": float(np.mean(times)),
                "std_seconds": float(np.std(times)),
                "min_seconds": float(np.min(times)),
                "max_seconds": float(np.max(times)),
                "sparse": sparse,
                "mode": mode,
            }
            rows.append(row)
            print(
                f"N={N}, a={a}, qubits={total_qubits}: "
                f"mean={row['mean_seconds']:.4f}s, std={row['std_seconds']:.4f}s, "
                f"range=[{row['min_seconds']:.4f}, {row['max_seconds']:.4f}]"
            )
        else:
            print(f"N={N}, a={a}: all runs failed")

    os.makedirs(os.path.dirname(output_csv) or ".", exist_ok=True)
    fieldnames = [
        "N",
        "a",
        "qubits",
        "repeats",
        "successes",
        "mean_seconds",
        "std_seconds",
        "min_seconds",
        "max_seconds",
        "sparse",
        "mode",
    ]
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Benchmark CSV saved as: {output_csv}")
    return rows


def run_runtime_analysis(
    test_cases: list[tuple[int, int]],
    repeats: int = 3,
    sparse: bool = True,
    mode: str = "distribution",
    output_dir: str = "images",
) -> tuple[list[int], list[int], list[float], list[float]]:
    """Run Shor's algorithm for different (N, a) and plot runtimes."""
    plt = get_pyplot()
    N_values = []
    qubits_required = []
    runtimes = []
    std_deviations = []

    print("Measuring Code Runtimes")
    for N, a in test_cases:
        # Run multiple times and take averages
        times = []

        for run in range(repeats):
            runtime = timer(N, a, sparse, mode=mode)
            if runtime is not None:
                times.append(runtime)

        if times:
            avg_runtime = np.mean(times)
            std_runtime = np.std(times)
            total_qubits = 3 * ceil(log2(N))

            N_values.append(N)
            qubits_required.append(total_qubits)
            runtimes.append(avg_runtime)
            std_deviations.append(std_runtime)
            print(
                f"N={N} ({total_qubits} qubits): Average {avg_runtime:.4f}s (±{std_runtime:.4f}s)"
            )
            print("=" * 40)

        else:
            print(f"N={N}: Failed")

    # Create the plots
    plt.figure(figsize=(15, 10))

    # Plot Runtime vs N
    plt.subplot(2, 2, 1)
    plt.errorbar(
        N_values,
        runtimes,
        yerr=std_deviations,
        fmt="bo-",
        linewidth=2,
        markersize=6,
        capsize=5,
        capthick=2,
        elinewidth=2,
    )
    plt.xlabel("N")
    plt.ylabel("Runtime (seconds)")
    plt.title("Shor's Algorithm Classical Simulation\nRuntime vs Semiprime N")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    # Plot Runtime vs Qubits Required
    plt.subplot(2, 2, 2)
    plt.errorbar(
        qubits_required,
        runtimes,
        yerr=std_deviations,
        fmt="ro-",
        linewidth=2,
        markersize=6,
        capsize=5,
        capthick=2,
        elinewidth=2,
    )
    plt.xlabel("Qubits")
    plt.ylabel("Runtime (seconds)")
    plt.title("Shor's Algorithm Classical Simulation\nRuntime vs Qubits Required")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(
        output_dir,
        f"runtime_vs_qubit_sparse_{sparse}_mode_{mode}_repeats_{repeats}.png",
    )
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"\nPlot saved as: {output_file}")

    # Close the main figure to free memory
    plt.close("all")

    return N_values, qubits_required, runtimes, std_deviations
