# Theory

A semiprime $N$ is the product of two primes $p$ and $q$.
For any integer $a < N$, the remainder when $a^x$ is divided by $N$, has period $r$ such that ```a ** (x + r) - a ** (x) = 0 mod N```.
Setting $x = 0$ gives:
``` a ** r = 1 mod N ```
which can be rearranged to write $N$ as a product of two smaller factors:
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

When we randomly pick a smaller integer $a$, there is a small chance that we directly get a factor.
If this is the case, then we simply pick another random integer until ```gcd(a, N) = 1```, meaning $a$ and $N$ are coprime.

If these conditions are satisfied, then we continue to the quantum part.

## Quantum Operations

We use two registers.
The first will be of size $n_qubits$, which is the smallest integer such that $2^{n_qubits} \leq N$.
For this project, the second register will have an equal number of qubits as the first.
The initial state is set to $00$.

### Hadamard Gates

Hadamard operators are used to create a superposition of all possible states, with equal amplitudes, for the first register only.
This is done by using ```numpy.kron``` to calculate the Kronecker product of multiple matrices.
The full Hadamard matrix is then multiplied with the identity matrix for the second register (also by using the Kronecker product).

# References

[https://en.m.wikipedia.org/wiki/Shor's_algorithm]
[https://en.m.wikipedia.org/wiki/RSA_cryptosystem]
