import numpy as np
from random import randint


def is_perfect_power(N):
    """Check if N is a perfect power."""
    for k in range(2, int(np.log2(N)) + 1):
        p = round(N ** (1 / k))
        if p ** k == N:
            return True, p, k
    return False, None, None


def classical_checks(N):
    """
    Performs classical checks for Shor's algorithm.

    Args:
        N: Coprime integer to factor
    """

    # Check if N is even
    if N % 2 == 0:
        factors = (2, N // 2)
        message = f'N is even. The factors are 2 and {N // 2}'
        return True, factors, message

    # Check if N is a perfect power
    is_power, base, exponent = is_perfect_power(N)
    if is_power:
        factors = (base, N // base)
        message = f'N is a perfect power: {N} = {base}^{exponent}. Base factor is {base}'
        return True, factors, message

    # Generate random integer between 2 and N-1
    a = randint(2, N - 1)

    # Check if gcd(a, N) > 1
    gcd_val = np.gcd(a, N)
    if gcd_val != 1:
        factors = (gcd_val, N // gcd_val)
        message = f'Lucky! gcd({a}, {N}) = {gcd_val}. The factors of N are: {gcd_val} and {N // gcd_val}'
        return True, factors, message
    else:
        message = f'Classical checks passed. a = {a}, gcd(a, N) = 1. Proceed to quantum part.'
        return False, None, message


# # Example usage:
# if __name__ == "__main__":
#     N = 15
#     success, factors, message = classical_checks(N)
#     print(message)
#
#     if success:
#         print(f"Factorization complete: {N} = {factors[0]} × {factors[1]}")
#     else:
#         print("Classical checks failed. Quantum algorithm needed.")
