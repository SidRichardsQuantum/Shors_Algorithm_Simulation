# Classical Simulation of Shor's Algorithm

A pure Python implementation of Shor's quantum factorization algorithm using classical matrix operations to simulate quantum circuits.
This project demonstrates the core concepts of Shor's algorithm without relying on quantum computing frameworks like Qiskit.

## Overview

Shor's algorithm is a quantum algorithm that efficiently finds the prime factors of large integers, which forms the basis for breaking RSA encryption.
This implementation simulates the quantum operations classically to illustrate how the algorithm works step-by-step.

## Algorithm Steps

1. **Input Validation**: Takes a coprime integer $N$ and checks that it isn't even or a perfect power
2. **Quantum Register Setup**: Creates two qubit registers
3. **Superposition**: Applies Hadamard gates to the first register to create quantum superposition with equal amplitudes
4. **Modular Exponentiation**: Implements an oracle unitary matrix to entangle the registers
5. **Quantum Fourier Transform**: Applies an inverse QFT matrix to extract period information
6. **Period Finding**: Analyzes measurement probabilities to determine period $r$
7. **Classical Post-Processing**: Uses the period to calculate prime factors

## Features

- **Pure Python Implementation**: No quantum computing libraries required
- **Educational Focus**: Clear step-by-step implementation with detailed comments
- **Visualization**: Plots probability distributions to visualize quantum measurements
- **Runtimes**: Graph of $N$ against code runtime to show the exponential nature of this classical simulation

## Installation

```bash
git clone https://github.com/SidRichardsQuantum/Shors_Algorithm_simulation
cd Shors_Algorithm_simulation
pip install -r requirements.txt
```

## Implementation Details

### Classical Checks
- Checks that $N$ is not trivial (even or a perfect power)
- Generates a random integer 2 < a < N

### Quantum Register Simulation
- Uses complex numpy arrays to represent quantum state vectors
- Implements qubit registers as tensor products of individual qubit states

### Quantum Gates
- **Hadamard Gates**: Creates an equal superposition of all states in the first register
- **Unitary Gate**: Implements modular exponentiation oracle
- **Inverse QFT**: Extracts period information from quantum state

### Classical Post-Processing
- Analyzes measurement probabilities to find period candidates
- Calculates both prime factors
- Verifies factors through classical division

## Limitations

- **Exponential Memory**: Classical simulation runtime is exponential for factorisation problems
- **Small Numbers Only**: Practical for factoring small integers (N < 100) using few qubits
- **Educational Purpose**: Not suitable for large numbers practically used for RSA
- **Multiple Runs**: May require multiple runs to find correct factors

## Mathematical Background

The algorithm relies on the mathematical relationship:
```
If a^r = 1 mod N, then a^(r/2) ± 1 gives are the two prime factors
```

Where:
- $N$ is the coprime (factor of two primes)
- $a$ is a randomly chosen integer less than $N$
- $r$ is the period of the function $f(x) = a^x mod N$

## Educational Resources

- [Shor's Algorithm Explained](https://en.wikipedia.org/wiki/Shor%27s_algorithm)
- [Quantum Fourier Transform](https://qiskit.org/textbook/ch-algorithms/quantum-fourier-transform.html)
- [Period Finding and Factorization](https://docs.microsoft.com/en-us/quantum/concepts/algorithms)

## Acknowledgments

This implementation is inspired by the original work of Peter Shor and serves as an educational tool for understanding quantum algorithms through classical simulation.

---

**Note**: This is a classical simulation for educational purposes.
Real quantum advantage requires actual quantum hardware or quantum simulators that can handle the exponential complexity efficiently.