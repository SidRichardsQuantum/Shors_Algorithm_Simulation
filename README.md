# Classical Simulation of Shor's Algorithm

A pure Python implementation of Shor's quantum factorization algorithm using classical matrix operations to simulate quantum circuits.
This project demonstrates the core concepts of Shor's algorithm without relying on quantum computing frameworks like Qiskit.

## Overview

Shor's algorithm is a quantum algorithm that efficiently finds the prime factors of large integers, which forms the basis for breaking RSA encryption.
This implementation simulates the quantum operations classically to illustrate how the algorithm works step-by-step.

We will use Qiskit to draw the quantum circuit, but nothing more.

## Algorithm Steps

1. **Input Validation**: Takes a semiprime and checks that it isn't even or a perfect power
2. **Quantum Register Setup**: Creates two qubit registers
3. **Equal Superposition**: Applies Hadamard gates to the first register to create quantum superposition with equal amplitudes
4. **Modular Exponentiation**: Implements an oracle unitary matrix to entangle the registers
5. **IQFT**: Applies an Inverse Quantum Fourier Transform matrix to extract period information
6. **Period Finding**: Analyzes measurement probabilities to determine period
7. **Classical Post-Processing**: Uses the period to calculate prime factors

See THEORY.md for a descriptive algorithm walkthrough.

## Features

- **Pure Python Implementation**: No quantum computing libraries required
- **Educational Focus**: Clear step-by-step implementation with detailed comments
- **Visualization**: Plots probability distributions to visualize quantum measurements
- **Runtimes**: Graph of code runtime to show the exponential nature of this classical simulation

## Installation

```bash
git clone https://github.com/SidRichardsQuantum/Shors_Algorithm_simulation
cd Shors_Algorithm_Simulation
pip install -r requirements.txt
```

## Implementation Details

- $N$ is the semiprime (factor of two primes)
- $a$ is an integer between $1$ and $N$
- $r$ is the period of the modular function ```a^x mod N```

### Classical Checks
- Checks that $N$ is not trivial (even or a perfect power)
- If $a$ is not specified, then a random integer is generated
- Verifies that ```gcd(a, N) = 1```

### Quantum Register Simulation
- Uses complex numpy arrays to represent quantum state vectors
- Implements qubit registers as tensor products of individual qubit states

### Quantum Gates
- **Hadamard**: Creates an equal superposition of all states in the first register
- **Unitary Oracle**: Implements modular exponentiation oracle to entangle the registers
- **IQFT**: Extracts period information from quantum state

### Classical Post-Processing
- Analyzes measurement probabilities to find period candidates
- Checks that $r$ is even
- Calculates prime factors $gcd(a^{r/2} \pm 1, N)$
- Verifies the factors are non-trivial ($N$ and $1$)

### Graphs

- After applying the IQFT matrix, we plot the state probabilities against state-index to display periodicity
- Runtime is plotted against semiprimes and required qubits to show the exponential time-complexity

## Limitations

- **Exponential Memory**: Classical simulation runtime is (sub-)exponential for factorisation problems
- **Small Numbers Only**: Practical for factoring small integers ($N < 300$) using few qubits
- **Educational Purpose**: Not suitable for large numbers practically used for RSA
- **Multiple Runs**: May require multiple runs if classical checks on $N, a$ or $r$ fail

## Project Structure

```
Shors_Algorithm_Simulation
├── LICENSE                       # Project license
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── THEORY.md                     # Theoretical background
├── main.py                       # Main execution script
├── examples/                     # Example usage and demonstrations
│   ├── __init__.py
│   ├── example_15.py             # Default example
│   └── runtimes_test.py          # Runtime performance testing
├── images/                       # Generated visualizations of examples
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
    │   └── runtime_plot.py       # Runtime analysis plots
    └── quantum_part/             # Quantum operators
        ├── __init__.py
        ├── hadamard_matrix.py    # Hadamard gate implementation
        ├── oracle_matrix.py      # Modular exponentiation oracle
        ├── iqft_matrix.py        # Inverse QFT implementation
        └── run_quantum_gates.py  # Quantum circuit execution
```

## Educational Resources

- [Shor's Algorithm Explained](https://en.wikipedia.org/wiki/Shor%27s_algorithm)
- [Quantum Fourier Transform](https://qiskit.org/textbook/ch-algorithms/quantum-fourier-transform.html)
- [Period Finding and Factorization](https://docs.microsoft.com/en-us/quantum/concepts/algorithms)

## Acknowledgments

This implementation is inspired by the original work of Peter Shor and serves as an educational tool for understanding quantum algorithms through classical simulation.

---

**Note**: This is a classical simulation for educational purposes.
Real quantum advantage requires actual quantum hardware that can efficiently implement this factorisation algorithm in polynomial (in $log(N)$) time.

---

📘 Author: [Sid Richards]

<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" width="20" /> LinkedIn: [https://www.linkedin.com/in/sid-richards-21374b30b/]
