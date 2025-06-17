import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import numpy as np
from math import log2, ceil
import matplotlib.pyplot as plt
import matplotlib
import time
from main import shors_simulation


def timer(N, a, sparse=True):
    """Time a single Shor's algorithm simulation."""
    start_time = time.time()
    try:
        shors_simulation(N=N, a=a, show_plots=False, sparse=sparse)
        end_time = time.time()
        return end_time - start_time
    except Exception as e:
        print(f"Error with N={N}, a={a}: {e}")
        return None


def run_runtime_analysis(test_cases, repeats=3, sparse=True):
    """Run Shor's algorithm for different (N, a) and plot runtimes."""
    N_values = []
    qubits_required = []
    runtimes = []
    std_deviations = []

    print("Measuring Code Runtimes")
    for N, a in test_cases:
        # Run multiple times and take averages
        times = []
        
        for run in range(repeats):
            runtime = timer(N, a, sparse)
            if runtime is not None:
                times.append(runtime)
        
        if times:
            avg_runtime = np.mean(times)
            std_runtime = np.std(times)
            total_qubits = 2 * ceil(log2(N))
            
            N_values.append(N)
            qubits_required.append(total_qubits)
            runtimes.append(avg_runtime)
            std_deviations.append(std_runtime)
            print(f"N={N} ({total_qubits} qubits): Average {avg_runtime:.4f}s (±{std_runtime:.4f}s)")
            print("=" * 40)

        else:
            print(f"N={N}: Failed")
    
    # Create the plots
    matplotlib.use('Agg') # Use non-interactive backend
    plt.figure(figsize=(15, 10))
    
    # Plot Runtime vs N
    plt.subplot(2, 2, 1)
    plt.errorbar(N_values, runtimes, yerr=std_deviations,
                fmt='bo-', linewidth=2, markersize=6,
                capsize=5, capthick=2, elinewidth=2)
    plt.xlabel('N')
    plt.ylabel('Runtime (seconds)')
    plt.title("Shor's Algorithm Classical Simulation\nRuntime vs Semiprime N")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Plot Runtime vs Qubits Required
    plt.subplot(2, 2, 2)
    plt.errorbar(qubits_required, runtimes, yerr=std_deviations,
                fmt='ro-', linewidth=2, markersize=6,
                capsize=5, capthick=2, elinewidth=2)
    plt.xlabel('Qubits')
    plt.ylabel('Runtime (seconds)')
    plt.title("Shor's Algorithm Classical Simulation\nRuntime vs Qubits Required")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save the plot in images directory
    os.makedirs('images', exist_ok=True)
    output_file = f'images/runtime_vs_qubit_sparse_{sparse}_repeats_{repeats}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nPlot saved as: {output_file}")
    
    # Close the main figure to free memory
    plt.close('all')
    
    return N_values, qubits_required, runtimes, std_deviations
