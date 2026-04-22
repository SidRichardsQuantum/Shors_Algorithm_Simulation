# Classical Simulation of Shor's Algorithm

A pure Python implementation of Shor's quantum factorization algorithm using classical simulation of the period-finding step.
The project supports both explicit matrix simulation for very small inputs and a faster distribution-based simulation for the ideal first-register measurement probabilities.

## Table of Contents

1. [Overview](#overview)
2. [Algorithm Steps](#algorithm-steps)
3. [Features](#features)
4. [Project Structure](#project-structure)
5. [Installation](#installation)
6. [Example Usage](#example-usage)
7. [Limitations](#limitations)
8. [References](#references)
9. [Acknowledgments](#acknowledgments)

### Overview

Shor's algorithm is a quantum algorithm that efficiently finds the prime factors of large integers, which forms the basis for breaking RSA encryption.
This implementation simulates the quantum operations classically to illustrate how Shor's algorithm works step by step. `mode="matrix"` explicitly applies the simulated gates and grows exponentially in memory; `mode="distribution"` computes the same ideal first-register probability distribution without materializing the full matrices.

See [THEORY.md](THEORY.md) for a descriptive algorithm walkthrough.

See [CIRCUITS.md](CIRCUITS.md) for the register and circuit-diagram walkthrough.

See [RESULTS.md](RESULTS.md) for results and conclusions.

### Algorithm Steps

1. **Input Validation**: Takes a semiprime and checks it isn't even or a perfect square
2. **Quantum Register Setup**: Creates a period register of size `Q ~= N^2` and a function register large enough to store values modulo `N`
3. **Equal Superposition**: Applies Hadamard gates to the first register to create quantum superposition with equal amplitudes
4. **Modular Exponentiation**: Encodes `a^x mod N` in a reversible oracle to entangle the registers
5. **IQFT**: Applies an Inverse Quantum Fourier Transform matrix to extract period information
6. **Period Finding**: Uses continued fractions on high-probability measurements to recover and validate period candidates
7. **Classical Post-Processing**: Uses the period to calculate prime factors

A quantum circuit sketch for Shor's Algorithm using 8 qubits:

![quantum_circuit](images/quantum_circuit.png)

### Features

- **Pure Python Implementation**: No quantum computing libraries required for the simulator
- **Circuit Drawing**: Uses Qiskit to generate the illustrative circuit diagram
- **Educational Focus**: Clear step-by-step implementation with detailed comments
- **Visualization**: Plots probability distributions to visualize quantum measurements
- **Period-Finding Diagnostics**: Plots oracle periodicity, marked IQFT peaks, continued-fraction candidates, and mode comparisons
- **Runtimes**: Graph of code runtime to show the exponential nature of this classical simulation
- **Two Period-Finding Modes**:
  - `mode="distribution"` computes the ideal first-register measurement distribution directly, using the standard `Q ~= N^2` period register size.
  - `mode="matrix"` explicitly applies the simulated Hadamard, oracle, and IQFT matrices for very small inputs.

### Project Structure

```
Shors_Algorithm_Simulation
├── LICENSE                       # Project license
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── CIRCUITS.md                   # Circuit diagram walkthrough
├── THEORY.md                     # Theoretical background
├── RESULTS.md                    # Results, conclusions and evaluations
├── main.py                       # Main execution script
├── examples/                     # Example usage and demonstrations
│   ├── __init__.py
│   ├── benchmark_runtime.py      # Save runtime benchmark table
│   ├── circuit_diagrams_example.py # Generate Qiskit circuit diagrams
│   ├── factorisation_example.py  # Single deterministic run with saved plot
│   ├── no_plot_example.py        # Deterministic run without displaying plots
│   ├── multiple_cases_example.py # Run several (N, a) examples without plots
│   ├── visualizations_example.py # Generate educational period-finding plots
│   └── runtimes_test.py          # Runtime performance testing
├── images/                       # Generated visualizations of examples
├── tests/                        # Regression tests
└── src/                          # Source code
    ├── __init__.py               # Main package initialization
    ├── classical_parts/          # Classical algorithm components
    │   ├── __init__.py
    │   ├── pre_checks.py         # Pre-quantum validation
    │   └── post_checks.py        # Post-quantum validation
    ├── plots_and_period/         # Visualization and period finding
    │   ├── __init__.py
    │   ├── find_period.py        # Period finding function
    │   ├── probability_plot.py   # Probability visualization
    │   ├── visualizations.py     # Educational diagnostics and comparison plots
    │   └── runtime_plot.py       # Runtime analysis plots
    └── quantum_part/             # Quantum operators
        ├── __init__.py
        ├── circuit_diagrams.py   # Reusable Qiskit circuit diagram builders
        ├── hadamard_matrix.py    # Hadamard gate implementation
        ├── oracle_matrix.py      # Modular exponentiation oracle
        ├── iqft_matrix.py        # Inverse QFT implementation
        ├── quantum_circuit.py    # Qiskit circuit diagram generation
        └── run_quantum_gates.py  # Quantum circuit execution
```

### Installation

```bash
git clone https://github.com/SidRichardsQuantum/Shors_Algorithm_Simulation
cd Shors_Algorithm_Simulation
pip install -r requirements.txt
```

`qiskit` and `pylatexenc` are included so `src/quantum_part/quantum_circuit.py` can regenerate the illustrative circuit diagram.

### Example Usage

**Terminal inputs**:

```python
python examples/factorisation_example.py   # single run with plot output
python examples/no_plot_example.py         # single run without plotting
python examples/multiple_cases_example.py  # batch of small deterministic cases
python examples/visualizations_example.py  # generate educational diagnostic plots
python examples/circuit_diagrams_example.py --N 15 --a 2
```

**Command-line usage**:

```bash
python main.py --N 35 --a 2 --mode distribution --plots
python main.py --N 15 --a 2 --mode matrix --json
```

Visualization plots can also be selected from the command line:

```bash
python examples/visualizations_example.py --N 35 --a 2 --plots oracle marked continued
python examples/visualizations_example.py --plots comparison --comparison-N 15 --comparison-a 2
```

Circuit diagrams can be generated from the command line:

```bash
python examples/circuit_diagrams_example.py --N 15 --a 2 --output-dir images
python -m src.quantum_part.circuit_diagrams --N 35 --a 2
```

**Programmatic mode selection**:

```python
from main import shors_simulation

result = shors_simulation(N=21, a=2, show_plots=False, mode="distribution")
print(result["success"], result["factors"], result["period"])

matrix_result = shors_simulation(N=15, a=2, show_plots=False, mode="matrix")
print(matrix_result["success"], matrix_result["factors"], matrix_result["period"])
```

`distribution` mode is the default and is appropriate for the documented examples. `matrix` mode is intended for the smallest cases because explicit gate matrices grow quickly.
`shors_simulation` returns a dictionary containing `success`, `N`, `a`, `mode`, `period`, `factors`, `message`, and `classical_precheck`.

**Output**:

```
N = 35
Running Classical Checks...
Classical checks passed.
a = 2.
Proceeding to quantum algorithm...
The period r = 12 is even.
a^(r/2) + 1 = 30, and gcd(30, 35) = 5
a^(r/2) - 1 = 28, and gcd(28, 35) = 7
The factors of N = 35 are 5 and 7.
```
This also saves the plot to the "images" directory as "first_register_probabilities_N=35_a=2.png":

![first-register probabilities for N=35, a=2](images/first_register_probabilities_N=35_a=2.png)

### Visualizations

`examples/visualizations_example.py` generates:

- oracle period pattern: `x -> a^x mod N`
- first-register probabilities with expected period peak markers
- continued-fraction candidate plot and CSV table
- matrix mode vs distribution mode comparison for a small case

### Tests

```bash
pytest -q
```

### Limitations

- **Exponential Runtime/Memory**: `mode="matrix"` scales exponentially with the number of simulated qubits and is only practical for tiny cases.
- **Distribution Mode Is Idealized**: `mode="distribution"` avoids full matrices by computing the ideal first-register distribution directly, which is still a classical simulation of the period-finding output.
- **Small Numbers Only**: Practical for factoring small educational examples, not cryptographic integers.
- **Educational Purpose**: Not suitable for large numbers practically used for low-bit RSA
- **Multiple Runs**: May require multiple runs if classical checks on $N, a$ or $r$ fail

### References

#### Algorithm and Theory

- [Peter W. Shor, "Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer" (arXiv)](https://arxiv.org/abs/quant-ph/9508027)
- [Published SIAM version of Shor's paper](https://doi.org/10.1137/S0097539795293172)
- [Nielsen and Chuang, "Quantum Computation and Quantum Information"](https://doi.org/10.1017/CBO9780511976667)
- [IBM Quantum Learning: Shor's algorithm](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/phase-estimation-and-factoring/shor-algorithm)

#### Implementation References

- [IBM Quantum: quantum circuit model](https://quantum.cloud.ibm.com/docs/en/api/qiskit/circuit)
- [Qiskit `QFTGate` API](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.QFTGate)
- [Qiskit `circuit_drawer` API](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.visualization.circuit_drawer)
- [Python `Fraction.limit_denominator`](https://docs.python.org/3/library/fractions.html#fractions.Fraction.limit_denominator)
- [NumPy inverse FFT](https://numpy.org/doc/stable/reference/generated/numpy.fft.ifft.html)
- [SciPy sparse CSR matrices](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html)
- [Matplotlib `savefig`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html)

### Acknowledgments

This implementation is inspired by the original work of Peter Shor and serves as an educational tool for understanding quantum algorithms through classical simulation.

**Note**: This is a classical simulation for educational purposes.
Real quantum advantage requires actual quantum hardware that can efficiently implement this factorisation algorithm in polynomial time (commonly cited as roughly $O((\log N)^3)$ for idealized gate complexity).

---

## Author

Sid Richards

- LinkedIn: [sid-richards-21374b30b](https://www.linkedin.com/in/sid-richards-21374b30b/)
- GitHub: [SidRichardsQuantum](https://github.com/SidRichardsQuantum)

## License

MIT. See [LICENSE](LICENSE).
