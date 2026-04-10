import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.plots_and_period.runtime_plot import benchmark_runtime_table


if __name__ == "__main__":
    """Benchmark selected deterministic cases and save a CSV summary."""
    benchmark_cases = [
        (15, 2),
        (21, 2),
        (33, 2),
        (35, 2),
    ]

    benchmark_runtime_table(
        test_cases=benchmark_cases,
        repeats=3,
        sparse=True,
        output_csv="images/runtime_benchmark_sparse_True_repeats_3.csv",
    )
