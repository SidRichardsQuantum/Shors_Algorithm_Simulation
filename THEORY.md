# Theory

A semiprime $N$ is the product of two primes $p$ and $q$.
For any integer $a < N$, the remainder when $a^x$ is divided by $N$, has period $r$ such that:
```
a ** (x + r) - a ** (x) = 0 mod N
```
Setting $x = 0$ gives ```a ** r = 1 mod N```, which can be rearranged to write $N$ as a product of two smaller factors:
```
(a ** (r / 2) + 1)(a ** (r / 2) - 1) = 0 mod N = N mod N
```
given that $r$ is even.

This makes factoring $N$ a period-finding problem, which Shor's algorithm solves in polynomial time.
Classical factorisation algorithms are exponentially complex for increasing $N$.

RSA encryption involves the generation of a public semiprime key, hence Shor's algorithm can be utilised to find the private decryption key to decrypt the corresponding messages.
Classical computers would take billions of years to break RSA-2048, but a quantum computer would take weeks!

## Classical Pre-Processing

There is no point running Shor's algorithm if $N$ is trivially even or a perfect power.
Therefore, we quickly checks that these conditions are both false.

When we randomly pick a smaller integer $a$, there is a small chance that we directly get $p$ or $q$.
If this is the case, then we simply pick another random integer until $gcd(a, N) = 1$, meaning $a$ and $N$ are coprime.

If these conditions are satisfied, then we continue to the quantum part.

## Quantum Operations

Two registers are used.
The first will be of size $n$, which is the smallest integer such that $2^n \geq N$.
For this project, the second register will have an equal number of qubits as the first.
The initial state is set to $|0⟩|0⟩$.

### Hadamard Gates

Hadamard operators are used to create a superposition of all possible states, with equal amplitudes, for the first register only.
A Hadamard matrix for one qubit is given as:
```
H = (1/√2) * [ [1,  1],
               [1, -1] ]
```
The Hadamard matrices are then applied to all qubits in the first register by iterating ```numpy.kron()``` - which calculates the Kronecker product of two matrices.
The full Hadamard matrix is then multiplied with the identity matrix (for the second register), also by using the Kronecker product.

### Modular Oracle

A unitary matrix $U$ which maps $|x⟩|y⟩ \rightarrow |x⟩|(y + a^x) mod N⟩$ is generated.
This leaves the first register unchanged, but entangles it with the second - while encoding periodicity.

### Inverse Quantum Fourier Transform (IQFT)

An IQFT matrix is constructed to make the amplitudes of the first register states periodic.
Peaks in probability form at every $2^n * k / r$, where $k$ is a non-negative integer.

In this project, probabilities are plotted against the state index to find the period $r$.
In a real implementation of Shor's algorithm, a measurement of the first register would have to be taken for a chance of finding $r$.
(I say "chance", because both $k$ and $r$ might be even - leading to degeneracy in what $r$ could be.)

## Classical Post Processing

For us to have $(a^{r/2} \pm 1)$, $r$ must be even.
If $r$ is not even, the algorithm needs to be restarted with a different random integer $a$.

## Default Example

The simplest example is factoring $N = 15$ into $3$ and $5$, as it is the smallest non-trivial semiprime.
Lets say $a = 7$, then we can see that $a^x mod N$ is periodic:
```
7 ** 0 mod 15 = 1
7 ** 1 mod 15 = 7
7 ** 2 mod 15 = 4
7 ** 3 mod 15 = 13
7 ** 4 mod 15 = 1
7 ** 5 mod 15 = 7
        ⋮
```
(Therefore, $r = 4$ for $a = 7$ and $N = 15$; but lets get the period from simulating Shor's algorithm!)

The smallest power of $2$ greater than $N$ is $16 = 2^4$, hence the number of qubits in the first register required is $n = 4$.
Therefore, the total number of qubits in the total register is $8$.

Applying a Hadamard operator on a qubit $|0⟩$ gives:
```
H|0⟩ = (1/√2) * (|0⟩ + |1⟩)
```
and applying $H$ on all qubits in the first register:
```
(H_1 ⊗ H_2 ⊗ H_3 ⊗ H_4)|0⟩ = (1 / 4) * (|0⟩ + |1⟩ + ... + |15⟩)
```
(However, in the python file quanutm_part.py, ```H_1 ⊗ H_2 ⊗ ... ⊗ H_n``` is multiplied with the itentity $I_{16 \times 16}$ to leave the second register unchanged.
This is a $256 \times 256$ matrix, which is already quite big considering this is the trivial example.)

Writing the unitary modular oracle operator as:
```
U = ∑∑(|x⟩|(y + a ** x) mod N⟩⟨y|⟨x|)
```
where both $\Sigma$s run from $0$ to $2^n - 1 = 15$; we can see that this maps:
```
|0⟩|y⟩ → |0⟩|y + 1⟩
|1⟩|y⟩ → |1⟩|y + 7⟩
       ⋮
|15⟩|y⟩ → |15⟩|y + 13⟩
```
The element $j, k$ is $1$, where $j$ and $k$ are the output and input states respectively.
```
j = x * 16 + (y + 7 ** x mod 15)
k = x * 16 + y
```
All other elements are $0$.

For the IQFT matrix, the element $j, k$ is:
```
(1 / 4) * exp(2πi * j * k / 16)
```
Applying this matrix increases the probabilities of measuring the states $|0⟩, |4⟩, |8⟩, |12⟩$, while decreasing those for all other states.
These state numbers are multiples of $4$ - which is the period $r$.

Post-processing checks will be passed, as $r$ is even; so there is no need to restart the algorithm with a different $a$.
Therefore, the factors are:
```
(a ** (r / 2)) + 1 mod N = (7 ** (4 / 2)) + 1 mod 15 = 5
(a ** (r / 2)) - 1 mod N = (7 ** (4 / 2)) - 1 mod 15 = 3
```
such that $15 = 5 * 3$.

# References

[https://en.m.wikipedia.org/wiki/Shor's_algorithm]
[https://en.m.wikipedia.org/wiki/RSA_cryptosystem]
