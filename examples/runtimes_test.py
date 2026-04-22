from shors_algorithm_simulation.plotting.runtime import run_runtime_analysis

if __name__ == "__main__":
    """Choose coprime (N, a) for non-trivial runs"""
    test_cases = [
        (15, 2),  # 3 * 5
        (21, 2),  # 3 * 7
        (33, 5),  # 3 * 11
        (35, 2),  # 5 * 7
        (39, 2),  # 3 * 13
        (51, 2),  # 3 * 17
        (55, 2),  # 5 * 11
        (57, 5),  # 3 * 19
        (65, 3),  # 5 * 13
        (69, 2),  # 3 * 23
        (77, 2),  # 7 * 11
        (85, 2),  # 5 * 17
        (87, 2),  # 3 * 29
        (91, 5),  # 7 * 13
        (93, 2),  # 3 * 31
        (95, 2),  # 5 * 19
        (111, 2),  # 3 * 37
        (115, 2),  # 5 * 23
        (119, 2),  # 7 * 17
        (123, 2),  # 3 * 41
        (129, 7),  # 3 * 43
        (133, 2),  # 7 * 19
        (141, 2),  # 3 * 47
        (161, 6),  # 7 * 23
    ]

    try:
        N_vals, qubits, times, stds = run_runtime_analysis(
            test_cases, 3, sparse=True, mode="distribution"
        )
        print("\nAnalysis complete!")

    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user.")

    except Exception as e:
        print(f"Error during analysis: {e}")
