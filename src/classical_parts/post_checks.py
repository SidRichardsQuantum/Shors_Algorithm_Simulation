import numpy as np


def post_checks(N, a, r):
    """Classically checks that r is even, then returns the factors."""
    if r % 2:
        print(f'The period r = {r} is even.')
        factors = (a ** (r // 2) + 1) % N, (a ** (r // 2) - 1) % N
        print(f'Therefore, N = ({a}^({r}/2) + 1) * ({a}^({r}/2) - 1) mod N = {factors[0]} * {factors[1]}')
        print(f'The factors of N = {15} are {factors[0]} and {factors[1]}.')
    else:
        print(f'r = {r} is not even. Run again with a != {a}.')
