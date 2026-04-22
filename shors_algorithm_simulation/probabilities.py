from __future__ import annotations

from collections import Counter
from math import ceil, log2

import numpy as np

from shors_algorithm_simulation.quantum.gates import run_quantum_gates


def compute_probs(
    N: int, a: int, sparse: bool = True, mode: str = "distribution"
) -> np.ndarray:
    """
    Compute first-register probabilities without plotting.

    Matrix mode builds and applies gates directly for tiny inputs. Distribution
    mode computes the same ideal first-register distribution without
    materializing the full matrices.
    """
    n_qubits = ceil(log2(N))
    Q = 2 ** (2 * n_qubits)
    M = 2**n_qubits

    if mode == "matrix":
        phi = run_quantum_gates(
            N,
            a,
            sparse=sparse,
            first_register_qubits=2 * n_qubits,
            second_register_qubits=n_qubits,
        )
        return np.sum(np.abs(phi.reshape(Q, M)) ** 2, axis=1)

    if mode != "distribution":
        raise ValueError("mode must be 'distribution' or 'matrix'")

    oracle_values = np.empty(Q, dtype=int)
    value = 1
    for x in range(Q):
        oracle_values[x] = value
        value = (value * a) % N

    prob_first_register = np.zeros(Q)
    for y in np.unique(oracle_values):
        indicator = (oracle_values == y).astype(float)
        amplitudes = np.fft.ifft(indicator)
        prob_first_register += np.abs(amplitudes) ** 2

    return prob_first_register


def sample_measurements(
    probabilities: np.ndarray,
    shots: int,
    random_seed: int | None = None,
) -> tuple[np.ndarray, dict[int, int]]:
    """Sample first-register measurements from an ideal probability vector."""
    rng = np.random.default_rng(random_seed)
    outcomes = rng.choice(
        len(probabilities), size=shots, p=probabilities / probabilities.sum()
    )
    counts = dict(sorted(Counter(int(outcome) for outcome in outcomes).items()))
    sampled_probabilities = np.zeros_like(probabilities, dtype=float)
    for outcome, count in counts.items():
        sampled_probabilities[outcome] = count / shots
    return sampled_probabilities, counts
