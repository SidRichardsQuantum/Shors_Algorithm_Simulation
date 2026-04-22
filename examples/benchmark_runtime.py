from shors_algorithm_simulation.plotting.runtime import benchmark_runtime_table

if __name__ == "__main__":
    """Benchmark selected deterministic cases and save a CSV summary."""
    benchmark_cases = [
        (15, 2),
        (21, 2),
        (33, 5),
        (35, 2),
    ]

    benchmark_runtime_table(
        test_cases=benchmark_cases,
        repeats=3,
        sparse=True,
        output_csv="images/runtime_benchmark_sparse_True_mode_distribution_repeats_3.csv",
        mode="distribution",
    )
