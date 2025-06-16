import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import numpy as np
import matplotlib.pyplot as plt
import time
from main import shors_simulation

# Set matplotlib backend for Codespaces
import matplotlib
matplotlib.use('Agg') # Use non-interactive backend


def calculate_qubits_required(N):
    """Calculate the number of qubits required for Shor's algorithm on N."""
    # For Shor's algorithm, we need approximately 2 * ceil(log2(N)) qubits
    # This is a simplified estimation - the actual implementation might vary
    import math
    return 2 * math.ceil(math.log2(N))


def time_shor_simulation(N, a, sparse=True):
    """Time a single Shor's algorithm simulation."""
    start_time = time.time()
    try:
        shors_simulation(N=N, a=a, show_plots=False, sparse=sparse)
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
        (15, 2),   # 3 * 5, 8 qubits
        (21, 2),   # 3 * 7, 10 qubits
        (35, 2),   # 5 * 7, 12 qubits
        (55, 2),   # 5 * 11, 12 qubits
        (77, 2),   # 7 * 11, 14 qubits
        (91, 5),   # 7 * 13, 14 qubits
        (115, 2),  # 5 * 23, 14 qubits
        (161, 6)   # 7 * 23, 16 qubits
    ]
    
    N_values = []
    qubits_required = []
    runtimes = []
    std_deviations = []
    
    print("Measuring Code Runtimes")
    for N, a in test_cases:
        # Run multiple times and take average for more reliable results
        times = []
        num_runs = repeats
        
        for run in range(num_runs):
            runtime = time_shor_simulation(N, a, sparse)
            if runtime is not None:
                times.append(runtime)
        
        if times:
            avg_runtime = np.mean(times)
            std_runtime = np.std(times)
            qubits = calculate_qubits_required(N)
            
            N_values.append(N)
            qubits_required.append(qubits)
            runtimes.append(avg_runtime)
            std_deviations.append(std_runtime)
            
            print(f"N={N} ({qubits} qubits): Avg: {avg_runtime:.4f}s (±{std_runtime:.4f}s)")
            print("=" * 40)
        else:
            print(f"N={N}: Failed")
    
    # Create the plots
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Runtime vs N
    plt.subplot(2, 2, 1)
    plt.errorbar(N_values, runtimes, yerr=std_deviations,
                fmt='bo-', linewidth=2, markersize=6,
                capsize=5, capthick=2, elinewidth=2)
    plt.xlabel('N (Semiprime to Factor)')
    plt.ylabel('Runtime (seconds)')
    plt.title("Runtime vs Semiprime (N)")
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Runtime vs Qubits Required
    plt.subplot(2, 2, 2)
    plt.errorbar(qubits_required, runtimes, yerr=std_deviations,
                fmt='ro-', linewidth=2, markersize=6,
                capsize=5, capthick=2, elinewidth=2)
    plt.xlabel('Qubits Required')
    plt.ylabel('Runtime (seconds)')
    plt.title("Runtime vs Qubits Required")
    plt.grid(True, alpha=0.3)
    
    # Plot 3: Combined view - N and Qubits on same plot
    plt.subplot(2, 1, 2)
    ax1 = plt.gca()
    
    # Plot runtime vs N
    line1 = ax1.errorbar(N_values, runtimes, yerr=std_deviations,
                        fmt='bo-', linewidth=2, markersize=6,
                        capsize=5, capthick=2, elinewidth=2,
                        label='Runtime vs N')
    ax1.set_xlabel('N (Semiprime to Factor)')
    ax1.set_ylabel('Runtime (seconds)', color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.grid(True, alpha=0.3)
    
    # Create second y-axis for qubits
    ax2 = ax1.twinx()
    line2 = ax2.plot(N_values, qubits_required, 'ro-', linewidth=2, markersize=6,
                    label='Qubits Required')
    ax2.set_ylabel('Qubits Required', color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    
    # Add legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    plt.title("Shor's Algorithm Classical Simulation\nRuntime and Qubits vs Semiprime")
    
    plt.tight_layout()
    
    # Create images directory if it doesn't exist
    os.makedirs('images', exist_ok=True)
    
    # Save the plot with the specified naming convention
    output_file = f'images/runtime_vs_qubit_sparse_{sparse}_repeats_{repeats}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nPlot saved as: {output_file}")
    
    # Also save individual plots
    # Runtime vs N only
    plt.figure(figsize=(10, 6))
    plt.errorbar(N_values, runtimes, yerr=std_deviations,
                fmt='bo-', linewidth=2, markersize=6,
                capsize=5, capthick=2, elinewidth=2)
    plt.xlabel('N (Semiprime to Factor)')
    plt.ylabel('Runtime (seconds)')
    plt.title("Shor's Algorithm - Runtime vs Semiprime (N)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    output_file_n = f'images/runtime_vs_N_sparse_{sparse}_repeats_{repeats}.png'
    plt.savefig(output_file_n, dpi=300, bbox_inches='tight')
    plt.close()
    
    # Runtime vs Qubits only  
    plt.figure(figsize=(10, 6))
    plt.errorbar(qubits_required, runtimes, yerr=std_deviations,
                fmt='ro-', linewidth=2, markersize=6,
                capsize=5, capthick=2, elinewidth=2)
    plt.xlabel('Qubits Required')
    plt.ylabel('Runtime (seconds)')
    plt.title("Shor's Algorithm - Runtime vs Qubits Required")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    output_file_qubits = f'images/runtime_vs_qubits_only_sparse_{sparse}_repeats_{repeats}.png'
    plt.savefig(output_file_qubits, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Additional plots saved as:")
    print(f"  - {output_file_n}")
    print(f"  - {output_file_qubits}")
    
    # Close the main figure to free memory
    plt.close('all')
    
    return N_values, qubits_required, runtimes, std_deviations
