import numpy as np


def post_checks(N, a, r):
    """Classically checks that r is even, then returns the factors."""
    if r % 2 != 0:  # r is ODD
        return f'r = {r} is odd. Run again with different {a}.'
    
    # r is EVEN - calculate potential factors
    temp1 = (pow(a, r//2) + 1) % N
    temp2 = (pow(a, r//2) - 1) % N
    factor1 = np.gcd(temp1, N)
    factor2 = np.gcd(temp2, N)
    
    # Build the common part of the message
    base_message = (f'The period r = {r} is even.\n'
                   f'a^(r/2) + 1 = {temp1}, and gcd({temp1}, {N}) = {factor1}\n'
                   f'a^(r/2) - 1 = {temp2}, and gcd({temp2}, {N}) = {factor2}')
    
    # Check for non-trivial factors
    if factor1 > 1 and factor1 < N:
        return _build_factor_message(base_message, N, a, factor1, factor2)
    elif factor2 > 1 and factor2 < N:
        return _build_factor_message(base_message, N, a, factor2, factor1)
    else:
        return (f'r = {r} is even, however:\n'
               f'a^(r/2) + 1 = {temp1}, gcd({temp1}, {N}) = {factor1}.\n'
               f'We have found the trivial factors {N} and {1}... This is trivial.\n'
               f'Try a value of a != {a}.')


def _build_factor_message(base_message, N, a, primary_factor, secondary_factor):
    """Helper function to build the factor message."""
    factors = (primary_factor, secondary_factor)
    
    if N == primary_factor * secondary_factor:
        return (f'{base_message}\n'
               f'The factors of N = {N} are {factors[0]} and {factors[1]}.')
    else:
        return (f'{base_message}\n'
               f'The factors of N = {N} are not {factors[0]} and {factors[1]}.\n'
               f'This is incorrect. Try a value of a != {a}.')
