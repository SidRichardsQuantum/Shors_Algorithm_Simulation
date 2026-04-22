from __future__ import annotations

import numpy as np
from fractions import Fraction
from shors_algorithm_simulation.probabilities import compute_probs


def find_period(
    N: int, a: int, sparse: bool = True, mode: str = "distribution"
) -> tuple[int, np.ndarray]:
    """
    Find a useful period using continued fractions.

    Shor's first register is measured at values close to s * Q / r, where
    Q ~= N^2 and r is the period. The measured fraction c / Q is converted
    into period candidates with continued fractions, and only candidates
    that produce non-trivial factors are accepted.
    """

    prob_first_register = compute_probs(N, a, sparse=sparse, mode=mode)

    for candidate in _iter_period_candidate_diagnostics(N, a, prob_first_register):
        for r in candidate["tested_periods"]:
            if _valid_period_for_factors(N, a, r):
                return r, prob_first_register

    raise ValueError(
        f"Could not find a validated period for N={N}, a={a}. Try a different a."
    )


def period_candidate_diagnostics(
    N: int,
    a: int,
    probabilities: np.ndarray,
    top_n: int | None = 12,
) -> list[dict[str, object]]:
    """Return continued-fraction period candidates ordered by measurement probability."""
    rows = []
    for row in _iter_period_candidate_diagnostics(N, a, probabilities):
        rows.append(row)
        if top_n is not None and len(rows) >= top_n:
            break

    return rows


def _iter_period_candidate_diagnostics(N: int, a: int, probabilities: np.ndarray):
    """Yield continued-fraction period candidates ordered by measurement probability."""
    Q = len(probabilities)
    candidate_indices = np.argsort(probabilities)[::-1]

    for measured_value in candidate_indices:
        probability = probabilities[measured_value]
        if measured_value == 0 or probability == 0:
            continue

        fraction = Fraction(int(measured_value), Q).limit_denominator(N)
        tested_periods = list(_period_candidates(fraction.denominator, N))
        valid_periods = [
            r for r in tested_periods if _valid_period_for_factors(N, a, r)
        ]

        yield {
            "measured_value": int(measured_value),
            "probability": float(probability),
            "fraction": fraction,
            "denominator": fraction.denominator,
            "tested_periods": tested_periods,
            "valid_periods": valid_periods,
            "accepted": bool(valid_periods),
        }


def _period_candidates(denominator: int, N: int):
    """Yield a continued-fraction denominator and its possible multiples."""
    if denominator <= 0:
        return

    for multiplier in range(1, (N // denominator) + 1):
        yield denominator * multiplier


def _valid_period_for_factors(N: int, a: int, r: int) -> bool:
    """A useful Shor period must recover non-trivial factors of N."""
    if r <= 0 or r % 2 != 0:
        return False

    if pow(a, r, N) != 1:
        return False

    factor1 = np.gcd(pow(a, r // 2, N) - 1, N)
    factor2 = np.gcd(pow(a, r // 2, N) + 1, N)

    return 1 < factor1 < N and 1 < factor2 < N and factor1 * factor2 == N
