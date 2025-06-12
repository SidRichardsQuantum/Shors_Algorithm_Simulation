# Theory

A semiprime $N$ is the product of two primes $p$ and $q$.
For any integer $a < N$, the remainder of $a^x / N$ is periodic with period $r$, such that $a^{x + r} - a^{x} = 0 mod N$.
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


# References

[https://en.m.wikipedia.org/wiki/Shor's_algorithm]
[https://en.m.wikipedia.org/wiki/RSA_cryptosystem]
