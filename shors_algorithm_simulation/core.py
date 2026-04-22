from __future__ import annotations

from math import gcd
from random import Random
from typing import Literal, TypedDict

import numpy as np

from shors_algorithm_simulation.period import find_period, period_candidate_diagnostics
from shors_algorithm_simulation.probabilities import compute_probs, sample_measurements
from shors_algorithm_simulation.validation import pre_checks

Mode = Literal["distribution", "matrix"]


class AttemptResult(TypedDict):
    """Structured result for one selected base a."""

    success: bool
    N: int
    a: int | None
    mode: Mode
    period: int | None
    factors: tuple[int, int] | None
    message: str
    classical_precheck: bool
    shots: int | None
    measurement_counts: dict[int, int] | None


class ShorsResult(AttemptResult):
    """Structured result for a full Shor simulation run."""

    attempts: list[AttemptResult]


def shors_simulation(
    N: int = 15,
    a: int | None = None,
    sparse: bool = True,
    mode: Mode = "distribution",
    max_attempts: int = 1,
    shots: int | None = None,
    random_seed: int | None = None,
) -> ShorsResult:
    """
    Run Shor's algorithm simulation and return structured data without printing.

    Args:
        N: Composite integer to factor.
        a: Optional base for modular exponentiation. If provided, only this base
           is attempted.
        sparse: Whether matrix mode should use sparse matrices.
        mode: "distribution" computes ideal probabilities directly; "matrix"
           explicitly applies simulated gates for tiny inputs.
        max_attempts: Number of candidate bases to try when a is not provided.
        shots: Optional number of sampled first-register measurements to use for
           continued-fraction recovery. If None, exact probabilities are used.
        random_seed: Optional seed for deterministic base selection and sampling.
    """
    _validate_inputs(N, a, max_attempts, shots)

    candidate_bases = [a] if a is not None else _candidate_bases(N, max_attempts, random_seed)
    attempts = []

    for candidate_a in candidate_bases:
        attempt = _run_single_attempt(
            N=N,
            a=candidate_a,
            sparse=sparse,
            mode=mode,
            shots=shots,
            random_seed=random_seed,
        )
        attempts.append(attempt)
        if attempt["success"]:
            return _with_attempts(attempt, attempts)

    result = attempts[-1]
    if len(attempts) > 1:
        result = dict(result)
        result["message"] = f"No successful factorization after {len(attempts)} attempts."

    return _with_attempts(result, attempts)


def json_ready(result: ShorsResult) -> dict[str, object]:
    """Convert tuple and integer-keyed values to JSON-friendly structures."""
    return _json_ready_value(result)


def recover_factors_from_period(N: int, a: int, r: int | None) -> tuple[int, int] | None:
    """Recover non-trivial factors from a validated period."""
    if r is None or r % 2 != 0:
        return None

    half_power = pow(a, r // 2, N)
    factor1 = gcd(half_power + 1, N)
    factor2 = gcd(half_power - 1, N)

    if 1 < factor1 < N and 1 < factor2 < N and factor1 * factor2 == N:
        return (factor1, factor2)

    return None


def validate_inputs(
    N: int,
    a: int | None = None,
    max_attempts: int = 1,
    shots: int | None = None,
) -> None:
    """Validate user-facing inputs before running classical or quantum steps."""
    _validate_inputs(N, a, max_attempts, shots)


def _run_single_attempt(
    N: int,
    a: int,
    sparse: bool,
    mode: Mode,
    shots: int | None,
    random_seed: int | None,
) -> AttemptResult:
    success, value, message = pre_checks(N, a)

    if success:
        factors = tuple(int(factor) for factor in value)
        return _build_attempt_result(
            success=True,
            N=N,
            a=a,
            mode=mode,
            factors=factors,
            period=None,
            message=message,
            classical_precheck=True,
            shots=shots,
            measurement_counts=None,
        )

    checked_a = int(value)

    counts = None
    try:
        period, probabilities, counts = _find_period_with_optional_sampling(
            N=N,
            a=checked_a,
            sparse=sparse,
            mode=mode,
            shots=shots,
            random_seed=random_seed,
        )
    except (ValueError, MemoryError) as error:
        return _build_attempt_result(
            success=False,
            N=N,
            a=checked_a,
            mode=mode,
            factors=None,
            period=None,
            message=str(error),
            classical_precheck=False,
            shots=shots,
            measurement_counts=counts,
        )

    factors = recover_factors_from_period(N, checked_a, period)
    if factors is None:
        message = f"Recovered period r={period}, but it did not produce non-trivial factors."
    else:
        message = _factor_message(N, checked_a, period, factors)

    return _build_attempt_result(
        success=factors is not None,
        N=N,
        a=checked_a,
        mode=mode,
        factors=factors,
        period=period,
        message=message,
        classical_precheck=False,
        shots=shots,
        measurement_counts=counts,
    )


def _find_period_with_optional_sampling(
    N: int,
    a: int,
    sparse: bool,
    mode: Mode,
    shots: int | None,
    random_seed: int | None,
) -> tuple[int, np.ndarray, dict[int, int] | None]:
    if shots is None:
        period, probabilities = find_period(N, a, sparse=sparse, mode=mode)
        return period, probabilities, None

    probabilities = compute_probs(N, a, sparse=sparse, mode=mode)
    sampled_probabilities, counts = sample_measurements(probabilities, shots, random_seed)

    for candidate in period_candidate_diagnostics(N, a, sampled_probabilities, top_n=None):
        valid_periods = candidate["valid_periods"]
        if valid_periods:
            return valid_periods[0], sampled_probabilities, counts

    raise ValueError(
        f"Could not find a validated period for N={N}, a={a} from {shots} sampled measurements. "
        "Try more shots or a different a."
    )


def _candidate_bases(N: int, max_attempts: int, random_seed: int | None) -> list[int]:
    candidates = list(range(2, N))
    rng = Random(random_seed)
    rng.shuffle(candidates)
    return candidates[:max_attempts]


def _validate_inputs(N: int, a: int | None, max_attempts: int, shots: int | None) -> None:
    if isinstance(N, bool) or not isinstance(N, int) or N <= 1:
        raise ValueError("N must be an integer greater than 1.")

    if _is_prime(N):
        raise ValueError("N must be composite; prime inputs do not have non-trivial factors.")

    if a is not None and (isinstance(a, bool) or not isinstance(a, int)):
        raise ValueError("a must be an integer when provided.")

    if a is not None and not (2 <= a <= N - 1):
        raise ValueError(f"Invalid value for 'a': {a}. Must be between 2 and {N - 1} (inclusive).")

    if isinstance(max_attempts, bool) or not isinstance(max_attempts, int) or max_attempts < 1:
        raise ValueError("max_attempts must be an integer greater than or equal to 1.")

    if shots is not None and (isinstance(shots, bool) or not isinstance(shots, int) or shots < 1):
        raise ValueError("shots must be an integer greater than or equal to 1 when provided.")


def _is_prime(value: int) -> bool:
    if value <= 1:
        return False
    if value <= 3:
        return True
    if value % 2 == 0:
        return False

    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2

    return True


def _factor_message(N: int, a: int, period: int, factors: tuple[int, int]) -> str:
    half_power = pow(a, period // 2, N)
    plus_value = half_power + 1
    minus_value = half_power - 1
    factor1 = gcd(plus_value, N)
    factor2 = gcd(minus_value, N)
    return (
        f"The period r = {period} is even.\n"
        f"a^(r/2) + 1 = {plus_value}, and gcd({plus_value}, {N}) = {factor1}\n"
        f"a^(r/2) - 1 = {minus_value}, and gcd({minus_value}, {N}) = {factor2}\n"
        f"The factors of N = {N} are {factors[0]} and {factors[1]}."
    )


def _build_attempt_result(
    success: bool,
    N: int,
    a: int | None,
    mode: Mode,
    factors: tuple[int, int] | None,
    period: int | None,
    message: str,
    classical_precheck: bool,
    shots: int | None,
    measurement_counts: dict[int, int] | None,
) -> AttemptResult:
    return {
        "success": success,
        "N": N,
        "a": a,
        "mode": mode,
        "period": period,
        "factors": factors,
        "message": message,
        "classical_precheck": classical_precheck,
        "shots": shots,
        "measurement_counts": measurement_counts,
    }


def _with_attempts(result: AttemptResult, attempts: list[AttemptResult]) -> ShorsResult:
    full_result = dict(result)
    full_result["attempts"] = attempts
    return full_result


def _json_ready_value(value: object) -> object:
    if isinstance(value, tuple):
        return [_json_ready_value(item) for item in value]
    if isinstance(value, list):
        return [_json_ready_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_ready_value(item) for key, item in value.items()}
    return value
