import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.plots_and_period.runtime_plot import run_runtime_analysis


if __name__ == "__main__":
    try:
        N_vals, qubits, times, stds = run_runtime_analysis(1, sparse=True)
        print("\nRuntime analysis complete!")
        
        # # Print summary statistics
        # print(f"\nSummary:")
        # print(f"N values tested: {N_vals}")
        # print(f"Qubits required: {qubits}")
        
    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user.")
    except Exception as e:
        print(f"Error during analysis: {e}")
