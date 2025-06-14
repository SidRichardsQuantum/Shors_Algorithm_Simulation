import numpy as np


def post_checks(N, a, r):
    """Classically checks that r is even, then returns the factors."""

    if r % 2 == 0:  # r is EVEN
        # Calculate the potential factors using GCD
        temp1 = a ** (r // 2) + 1
        temp2 = a ** (r // 2) - 1
        factor1 = np.gcd(temp1, N)
        factor2 = np.gcd(temp2, N)

        # Check if we found non-trivial factors
        if factor1 > 1 and factor1 < N:
            other_factor = N // factor1
            factors = (factor1, other_factor)
            message = (f'The period r = {r} is even.'
                       f'\na^(r/2) + 1 = {temp1}, and gcd({temp1}, {N}) = {factor1}'
                       f'\na^(r/2) - 1 = {temp2}, and gcd({temp2}, {N}) = {factor2}'
                       f'\nThe factors of N = {N} are {factors[0]} and {factors[1]}.')

        elif factor2 > 1 and factor2 < N:
            other_factor = N // factor2
            factors = (factor2, other_factor)
            message = (f'The period r = {r} is even.'
                       f'\na^(r/2) + 1 = {temp1}, gcd({temp1}, {N}) = {factor1}'
                       f'\na^(r/2) - 1 = {temp2}, gcd({temp2}, {N}) = {factor2}'
                       f'\nThe factors of N = {N} are {factors[0]} and {factors[1]}.')

        else:
            message = (f'r = {r} is even, however:'
                       f'\na^(r/2) + 1 = {temp1}, gcd({temp1}, {N}) = {factor1}... This is N.'
                       f'\nWe have found the trivial factors {15} and {1}.'
                       f'\nTry a value of a != {a}.')

    else:  # r is ODD
        message = f'r = {r} is odd. Run again with different {a}.'

    return message
