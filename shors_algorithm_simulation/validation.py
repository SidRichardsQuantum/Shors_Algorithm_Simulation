from __future__ import annotations

from random import randint

import numpy as np


def is_perfect_power(N: int) -> tuple[bool, int | None, int | None]:
    """Check if N is a perfect power."""
    for k in range(2, int(np.log2(N)) + 1):
        p = round(N ** (1 / k))
        if p ** k == N:
            return True, p, k
    return False, None, None


def pre_checks(N: int, a: int | None = None) -> tuple[bool, tuple[int, int] | int, str]:
    """
    Perform classical pre-checks for Shor's algorithm.

    Returns (True, factors, message) if classical work already factors N.
    Returns (False, a, message) when period finding should continue.
    """
    if N % 2 == 0:
        factors = (2, N // 2)
        message = (
            f"N is even. The factors are 2 and {N // 2}"
            "\nClassical methods found factors!\nNo quantum computation needed."
        )
        return True, factors, message

    is_power, base, exponent = is_perfect_power(N)
    if is_power and base is not None:
        factors = (base, N // base)
        message = (
            f"N is a perfect power: {N} = {base}^{exponent}."
            "\nClassical methods found factors!\nNo quantum computation needed."
        )
        return True, factors, message

    checked_a = a if a is not None else randint(2, N - 1)

    gcd_val = int(np.gcd(checked_a, N))
    if gcd_val != 1:
        factors = (gcd_val, N // gcd_val)
        message = (
            f"gcd(N, a) = gcd({N}, {checked_a}) = {gcd_val}.\n"
            f"The factors of N are: {gcd_val} and {N // gcd_val}"
            "\nClassical methods found factors!\nNo quantum computation needed."
        )
        return True, factors, message

    message = f"Classical checks passed.\na = {checked_a}."
    return False, checked_a, message


def post_checks(N: int, a: int, r: int) -> str:
    """Classically check a recovered period and return a human-readable message."""
    if r % 2 != 0:
        return f"r = {r} is odd. Run again with different {a}."

    temp1 = (pow(a, r // 2) + 1) % N
    temp2 = (pow(a, r // 2) - 1) % N
    factor1 = int(np.gcd(temp1, N))
    factor2 = int(np.gcd(temp2, N))

    base_message = (
        f"The period r = {r} is even.\n"
        f"a^(r/2) + 1 = {temp1}, and gcd({temp1}, {N}) = {factor1}\n"
        f"a^(r/2) - 1 = {temp2}, and gcd({temp2}, {N}) = {factor2}"
    )

    if 1 < factor1 < N:
        return _build_factor_message(base_message, N, a, factor1, factor2)
    if 1 < factor2 < N:
        return _build_factor_message(base_message, N, a, factor2, factor1)
    return (
        f"r = {r} is even, however:\n"
        f"a^(r/2) + 1 = {temp1}, gcd({temp1}, {N}) = {factor1}.\n"
        f"We have found the trivial factors {N} and {1}... This is trivial.\n"
        f"Try a value of a != {a}."
    )


def _build_factor_message(
    base_message: str,
    N: int,
    a: int,
    primary_factor: int,
    secondary_factor: int,
) -> str:
    factors = (primary_factor, secondary_factor)

    if N == primary_factor * secondary_factor:
        return f"{base_message}\nThe factors of N = {N} are {factors[0]} and {factors[1]}."
    return (
        f"{base_message}\n"
        f"The factors of N = {N} are not {factors[0]} and {factors[1]}.\n"
        f"This is incorrect. Try a value of a != {a}."
    )
