import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.plots_and_period.runtime_plot import run_runtime_analysis


if __name__ == "__main__":
    """Choose coprime (N, a) for non-trivial runs"""
    test_cases = [
    (15, 2),   # 3 * 5, 8 qubits
    (21, 2),   # 3 * 7, 10 qubits
    (33, 2),   # 3 * 11, 12 qubits
    (35, 2),   # 5 * 7, 12 qubits
    (39, 2),   # 3 * 13, 11 qubits
    (51, 2),   # 3 * 17, 12 qubits
    (55, 2),   # 5 * 11, 12 qubits
    (57, 5),   # 3 * 19, 12 qubits
    (65, 3),   # 5 * 13, 13 qubits
    (69, 2),   # 3 * 23, 13 qubits
    (77, 2),   # 7 * 11, 14 qubits
    (85, 2),   # 5 * 17, 13 qubits
    (87, 2),   # 3 * 29, 13 qubits
    (91, 5),   # 7 * 13, 14 qubits
    (93, 2),   # 3 * 31, 14 qubits
    (95, 2),   # 5 * 19, 14 qubits
    (111, 2),  # 3 * 37, 14 qubits
    (115, 2),  # 5 * 23, 14 qubits
    (119, 2),  # 7 * 17, 14 qubits
    (123, 2),  # 3 * 41, 14 qubits
    (129, 7),  # 3 * 43, 15 qubits
    (133, 2),  # 7 * 19, 15 qubits
    (141, 2),  # 3 * 47, 15 qubits
    (161, 6),  # 7 * 23, 16 qubits
]

    try:
        N_vals, qubits, times, stds = run_runtime_analysis(test_cases, 3, sparse=True)
        print("\nAnalysis complete!")
        
    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user.")

    except Exception as e:
        print(f"Error during analysis: {e}")
