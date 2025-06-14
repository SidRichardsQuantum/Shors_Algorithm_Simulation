import numpy as np
from random import randint


def is_perfect_power(N):
    """Check if N is a perfect power."""
    for k in range(2, int(np.log2(N)) + 1):
        p = round(N ** (1 / k))
        if p ** k == N:
            return True, p, k
    return False, None, None


def pre_checks(N, a=None):
    """
    Performs classical checks for Shor's algorithm.

    Args:
        N: Coprime integer to factor
    """

    # Check if N is even
    if N % 2 == 0:
        factors = (2, N // 2)
        message = (f'N is even. The factors are 2 and {N // 2}'
                   f'\nClassical methods found factors!\nNo quantum computation needed.')
        return True, factors, message

    # Check if N is a perfect power
    is_power, base, exponent = is_perfect_power(N)
    if is_power:
        factors = (base, N // base)
        message = (f'N is a perfect power: {N} = {base}^{exponent}.'
                   f'\nClassical methods found factors!\nNo quantum computation needed.')
        return True, factors, message

    # Use provided a or random integer between 2 and N - 1
    if a is not None:
        a = a
    else:
        a = randint(2, N - 1)  # Generate random a

    # Check if gcd(a, N) > 1
    gcd_val = np.gcd(a, N)
    if gcd_val != 1:
        factors = (gcd_val, N // gcd_val)
        message = (f'gcd(N, a) = gcd({N}, {a}) = {gcd_val}.\n'
                   f'The factors of N are: {gcd_val} and {N // gcd_val}'
                   f'\nClassical methods found factors!\nNo quantum computation needed.')
        return True, factors, message

    else:
        message = (f'Classical checks passed.'
                   f'\na = {a}.')
        return False, a, message
