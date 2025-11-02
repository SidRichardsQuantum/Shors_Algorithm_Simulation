# Theory

## Table of Contents

- [Intro](#intro)
- [Classical Pre-Processing](#classical-pre-processing)
- [Quantum Operations](#quantum-operations)
  - [Hadamard Gates](#hadamard-gates)
  - [Modular Oracle](#modular-oracle)
  - [Inverse Quantum Fourier Transform (IQFT)](#inverse-quantum-fourier-transform-iqft)
- [Classical Post Processing](#classical-post-processing)
- [Default Example](#default-example)
  - [Modular Periodicity](#modular-periodicity)
  - [Qubit Number](#qubit-number)
  - [Hadamard Matrix](#hadamard-matrix)
  - [Unitary Matrix](#unitary-matrix)
  - [IQFT Matrix](#iqft-matrix)
  - [Result](#result)
- [References](#references)

## Intro

A semiprime $N$ is the product of two primes.
For any integer $a < N$ coprime to $N$, and integer $b$, the function $a^x \bmod N$ has period $r$:
```
a^(b+r) ≡ a^b (mod N)
```
Setting $b = 0$ allows us to write $N$ as a product of two factors $\bmod N$:
```
a^r ≡ 1 (mod N)
a^r - 1 ≡ 0 (mod N)
(a^(r/2))^2 - 1 ≡ 0 (mod N)
(a^(r/2) - 1)(a^(r/2) + 1) ≡ 0 (mod N)
```
Hence the two products in the last line divide $N$.
Therefore, we can find the factors from by finding $r$ (given that it's even).
This makes factoring $N$ a period-finding problem, which Shor's algorithm solves in polynomial time - exponentially faster than classical algorithms.

RSA encryption involves the generation of a public semiprime key, hence Shor's algorithm can be utilised to find the private decryption key to decrypt the corresponding messages.
Classical computers would take billions of years to break RSA-2048, but a quantum computer would take months!

## Classical Pre-Processing

There is no point running Shor's algorithm if $N$ is trivially even or a perfect power.
Therefore, we quickly checks that these conditions are both false.

When we randomly pick a smaller integer $a$, there is a small chance that we directly get one of the factors.
If this is the case, then we simply pick another random integer until $\gcd(a, N) = 1$, meaning $a$ and $N$ are coprime.

If these conditions are satisfied, then we continue to the quantum part.

## Quantum Operations

Two registers are used.
The first will be of size $n$, which is the smallest integer such that $2^n \geq N$.
For this project, the second register will have an equal number of qubits as the first.
The initial state is set to ```|ψ0⟩ = |0⟩|0⟩```.

### Hadamard Gates

Hadamard operators are used to create a superposition of all possible states, with equal amplitudes, for the first register only.
A Hadamard matrix for one qubit is given as:
```
H = (1/√2) * [ [1,  1],
               [1, -1] ]
```
The Hadamard matrices are then applied to all qubits in the first register by iterating ```numpy.kron()``` - which calculates the Kronecker product of two matrices.
The full Hadamard matrix is then multiplied with the identity matrix (for the second register), also by using the Kronecker product.
Applying this to the full register gives:
```
|ψ1⟩ = (H^{⊗n} ⊗ I_{2^n})|ψ0⟩ = (1/√(2^n)) ∑_x |x⟩|0⟩
```

### Modular Oracle

A unitary matrix $U$ which maps $|x⟩|y⟩ \rightarrow |x⟩|(y + a^x) \bmod N⟩$ is generated.
Applying this to ```|ψ1⟩``` above gives:
```
|ψ2⟩ = U|ψ1⟩ = (1/√(2^n)) ∑_x |x⟩|a^x mod N⟩
```
This leaves the first register unchanged, but entangles it with the second - encoding periodicity.

### Inverse Quantum Fourier Transform (IQFT)

An IQFT matrix is constructed to make the amplitudes of the first register states periodic.
```
QFT^{-1}|x⟩ = (1/√(2^n)) ∑_k exp(2πi * x * k / 2^n)|k⟩
```
Peaks in probability form near states with index $s$, where $s / 2^n \approx t / r$ for integer values of $t$.

In a real implementation of Shor's algorithm using quantum hardware, a measurement of the first register would have to be taken for a chance of finding $r$.
(I say "chance", because both $t$ and $r$ might be even - leading to degeneracy in what $r$ could be.)

In this project, the first register state probabilities are plotted against the state index to display the period.
`find_period.py` then takes these probabilities and finds $r$ using the differences in state indices which have the highest probabilities.

## Classical Post Processing

$r$ must be even to calculate the factors $\gcd(a^{r/2} \pm 1, N)$.
If $r$ is not even, the algorithm needs to be restarted with a different integer $a$.
It is also possible for trivial factors $1$ and $N$ to be returned, such that the algorithm needs to be restarted with a different $a$.
Otherwise, the non-trivial prime factors are returned.

We also time the algorithm for different pairs of $(N, a)$ and plot runtimes against $N$ and the total number of required qubits $2n$.

# Default Example

### Modular Periodicity

The simplest example is factoring $N = 15$ into $3$ and $5$, as it is the smallest non-trivial semiprime.
Lets say $a = 7$, then we can see that $a^x \bmod N$ is periodic:
```
7^0 ≡ 1 (mod 15)
7^1 ≡ 7 (mod 15)
7^2 ≡ 4 (mod 15)
7^3 ≡ 13 (mod 15)
7^4 ≡ 1 (mod 15)
7^5 ≡ 7 (mod 15)
        ⋮
```
(We can see that $r = 4$ here; but lets get the period from simulating Shor's algorithm!)

### Qubit Number

The smallest power of $2$ greater than $N$ is $16 = 2^4$.
Therefore, the number of qubits in the first register required is $n = 4$ and the total number of qubits in the total register is $2n = 8$.

### Hadamard Matrix

Applying a Hadamard operator on a qubit $|0⟩$ gives:
```
H|0⟩ = (1/√2) * (|0⟩ + |1⟩)
```
and applying Hadamard operators on all qubits in the first register:
```
(H_1 ⊗ H_2 ⊗ H_3 ⊗ H_4)|0⟩ = (1 / 4) * (|0⟩ + |1⟩ + ... + |15⟩)
```
(However, in the file `quantum_part.py`, ```H_1 ⊗ H_2 ⊗ ... ⊗ H_n``` is multiplied with the identity $I_{16 \times 16}$ to leave the second register unchanged.
This is a $256 \times 256$ matrix, which is already quite big considering this is the trivial example.)

### Unitary Matrix

Writing the oracle unitary operator as:
```
U = ∑_x ∑_y |x⟩|(y + a^x) mod N⟩⟨y|⟨x|
```
where both $∑$ run from $0$ to $2^n - 1 = 15$.
This maps:
```
|0⟩|y⟩ → |0⟩|y + 1⟩
|1⟩|y⟩ → |1⟩|y + 7⟩
       ⋮
|15⟩|y⟩ → |15⟩|y + 13⟩
```
The non-zero elements $j, k$ are $1$, where $j$ and $k$ are the output and input states respectively.
Because $U$ targets the second register, $j$ and $k$ can be written as:
```
j = x * 16 + ((y + 7^x) mod 15)
k = x * 16 + y
```

### IQFT Matrix

This example's elements $j, k$ for the $QFT^{-1}$ matrix:
```
(1 / 4) * exp(2πi * j * k / 16)
```
Applying this matrix increases the probabilities of measuring the states $|0⟩, |4⟩, |8⟩, |12⟩$, while decreasing those for all other states.
These state numbers are multiples of $4$ - which is the period $r$.

### Result

Post-processing checks will be passed, so there is no need to restart the algorithm with a different $a$.
The products are:
```
(a^(r/2)) + 1 = (7^(4 / 2)) + 1 = 4 + 1 ≡ 5 (mod 15)
(a^(r/2)) - 1 = (7^(4 / 2)) - 1 = 4 - 1 ≡ 3 (mod 15)
```
such that $\gcd(3, 15) = 3$ and $\gcd(5, 15) = 5$ give the factors of $15$: $3$ and $5$.

## References

- [Shor's Algorithm Explained](https://en.wikipedia.org/wiki/Shor%27s_algorithm)
- [Quantum Fourier Transform](https://qiskit.org/textbook/ch-algorithms/quantum-fourier-transform.html)
- [Period Finding and Factorization](https://docs.microsoft.com/en-us/quantum/concepts/algorithms)

---

📘 Author: Sid Richards (SidRichardsQuantum)

<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" width="20" /> LinkedIn: https://www.linkedin.com/in/sid-richards-21374b30b/

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
