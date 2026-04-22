# Theory

## Table of Contents

- [Intro](#intro)
- [Classical Pre-Processing](#classical-pre-processing)
- [Quantum Period Finding](#quantum-period-finding)
  - [Registers](#registers)
  - [Hadamard Gates](#hadamard-gates)
  - [Modular Oracle](#modular-oracle)
  - [Inverse Quantum Fourier Transform](#inverse-quantum-fourier-transform)
  - [Continued Fractions](#continued-fractions)
- [Classical Post-Processing](#classical-post-processing)
- [Simulation Modes](#simulation-modes)
- [Example](#example)
- [References](#references)

## Intro

A semiprime $N$ is the product of two primes. For an integer $a < N$ coprime to $N$, the function

```
f(x) = a^x mod N
```

is periodic. Its period $r$ satisfies:

```
a^r == 1 (mod N)
```

If $r$ is even, then:

```
a^r - 1 == 0 (mod N)
(a^(r/2) - 1)(a^(r/2) + 1) == 0 (mod N)
```

This means non-trivial factors of $N$ may be recovered with:

```
gcd(a^(r/2) - 1, N)
gcd(a^(r/2) + 1, N)
```

The quantum part of Shor's algorithm is a period-finding routine. The classical post-processing then turns a useful period into factors.

## Classical Pre-Processing

Before simulating the quantum period-finding step, the code checks for easy classical cases:

- $N$ is even
- $N$ is a perfect power
- $\gcd(a, N) > 1$

If any of these checks finds factors, no quantum simulation is needed. Otherwise, the code proceeds with a coprime base $a$.

## Quantum Period Finding

### Registers

Let:

```
n = ceil(log2(N))
Q = 2^(2n)
M = 2^n
```

The simulator uses:

- a first register with `Q` states, corresponding to `2n` qubits
- a second register with `M` states, corresponding to `n` qubits

Using `Q ~= N^2` gives enough resolution for continued-fraction period recovery.

### Hadamard Gates

The first register starts in state $|0⟩$. Hadamard gates create an equal superposition over all first-register states:

```
|ψ1⟩ = (1/sqrt(Q)) sum_x |x⟩|0⟩
```

In `mode="matrix"`, this is represented by an explicit Hadamard matrix on the first register tensor an identity matrix on the second register.

### Modular Oracle

The oracle encodes the periodic function in the second register:

```
|x⟩|0⟩ -> |x⟩|a^x mod N⟩
```

The explicit matrix implementation uses a reversible XOR oracle:

```
|x⟩|y⟩ -> |x⟩|y xor (a^x mod N)⟩
```

This makes the oracle a permutation matrix and therefore unitary. Starting from $|y⟩ = |0⟩$, it produces the same encoded function values needed for period finding.

After the oracle, the state has the form:

```
|ψ2⟩ = (1/sqrt(Q)) sum_x |x⟩|a^x mod N⟩
```

### Inverse Quantum Fourier Transform

The inverse quantum Fourier transform is applied to the first register. It concentrates probability near values `c` satisfying:

```
c / Q ~= s / r
```

where:

- `r` is the period
- `s` is an integer
- `Q` is the first-register dimension

The resulting first-register probabilities are plotted by `probability_plot.py`.

### Continued Fractions

`find_period.py` sorts measurement outcomes by probability. For each high-probability measured value `c`, it forms:

```
c / Q
```

and uses continued fractions to recover denominator candidates. Candidate denominators and their multiples are accepted only if they pass validation:

```
pow(a, r, N) == 1
gcd(a^(r/2) - 1, N) and gcd(a^(r/2) + 1, N) are non-trivial factors
```

This replaces the earlier peak-spacing heuristic. It also correctly rejects cases where a period exists but cannot factor $N$, such as $N=33, a=2$.

## Classical Post-Processing

Once a useful period `r` is found, the code computes:

```
gcd(a^(r/2) - 1, N)
gcd(a^(r/2) + 1, N)
```

If both are non-trivial and multiply to $N$, factorization succeeds. Otherwise, Shor's algorithm must be retried with a different base $a$.

## Simulation Modes

The repository supports two period-finding modes:

- `mode="distribution"` computes the ideal first-register probability distribution directly. This is the default and is appropriate for the documented examples.
- `mode="matrix"` explicitly builds and applies the simulated Hadamard, oracle, and IQFT matrices. This is useful for tiny cases and for comparing against distribution mode.

For `N=15, a=2`, both modes produce matching first-register probabilities up to floating-point error.

## Example

For $N = 15$ and $a = 2$:

```
2^0 == 1  (mod 15)
2^1 == 2  (mod 15)
2^2 == 4  (mod 15)
2^3 == 8  (mod 15)
2^4 == 1  (mod 15)
```

The period is $r = 4$. Since $r$ is even:

```
2^(r/2) = 2^2 = 4
gcd(4 - 1, 15) = gcd(3, 15) = 3
gcd(4 + 1, 15) = gcd(5, 15) = 5
```

So the factors of $15$ are $3$ and $5$.

The visualization helpers can show:

- the repeated oracle pattern `a^x mod N`
- first-register probability peaks after IQFT
- continued-fraction candidates
- why a chosen base succeeds or must be retried

For register-flow diagrams and Qiskit-generated circuit drawings, see [CIRCUITS.md](CIRCUITS.md).

## References

### Primary Sources

- [Peter W. Shor, "Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer" (arXiv)](https://arxiv.org/abs/quant-ph/9508027)
- [Published SIAM version of Shor's paper](https://doi.org/10.1137/S0097539795293172)
- [Nielsen and Chuang, "Quantum Computation and Quantum Information"](https://doi.org/10.1017/CBO9780511976667)

### Algorithm Background

- [IBM Quantum Learning: Shor's algorithm](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/phase-estimation-and-factoring/shor-algorithm)
- [IBM Quantum tutorial: Shor's algorithm](https://quantum.cloud.ibm.com/docs/tutorials/shors-algorithm)
- [Wikipedia: Shor's algorithm](https://en.wikipedia.org/wiki/Shor%27s_algorithm)

### Implementation References

- [Python `Fraction.limit_denominator`](https://docs.python.org/3/library/fractions.html#fractions.Fraction.limit_denominator)
- [NumPy inverse FFT](https://numpy.org/doc/stable/reference/generated/numpy.fft.ifft.html)
- [SciPy sparse CSR matrices](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html)

---

## Author

Sid Richards

- LinkedIn: [sid-richards-21374b30b](https://www.linkedin.com/in/sid-richards-21374b30b/)
- GitHub: [SidRichardsQuantum](https://github.com/SidRichardsQuantum)

## License

MIT. See [LICENSE](LICENSE).
