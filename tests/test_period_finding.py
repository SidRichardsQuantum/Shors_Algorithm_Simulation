import numpy as np
import pytest

from shors_algorithm_simulation import compute_probs, sample_measurements, shors_simulation
from shors_algorithm_simulation.period import find_period
from shors_algorithm_simulation.plotting.diagnostics import (
    generate_visualization_set,
    plot_continued_fraction_diagnostics,
    plot_marked_probability_distribution,
    plot_matrix_distribution_comparison,
    plot_oracle_period_pattern,
)
from shors_algorithm_simulation.quantum.oracle import oracle_matrix_sparse


@pytest.mark.parametrize(
    ("N", "a", "expected_period"),
    [
        (15, 2, 4),
        (21, 2, 6),
        (33, 5, 10),
    ],
)
def test_find_period_recovers_useful_periods(N, a, expected_period):
    period, probabilities = find_period(N, a, mode="distribution")

    assert period == expected_period
    assert np.isclose(probabilities.sum(), 1.0)


def test_find_period_rejects_period_that_cannot_factor():
    with pytest.raises(ValueError, match="Could not find a validated period"):
        find_period(33, 2, mode="distribution")


@pytest.mark.parametrize("N", [0, 1, -15, 15.0, True])
def test_shors_simulation_rejects_invalid_N(N):
    with pytest.raises(ValueError, match="N must be an integer greater than 1"):
        shors_simulation(N=N, a=2)


def test_shors_simulation_rejects_prime_N():
    with pytest.raises(ValueError, match="N must be composite"):
        shors_simulation(N=17, a=2)


@pytest.mark.parametrize("a", [1, 15])
def test_shors_simulation_rejects_out_of_range_a(a):
    with pytest.raises(ValueError, match="Invalid value for 'a'"):
        shors_simulation(N=15, a=a)


@pytest.mark.parametrize("a", [2.5, False])
def test_shors_simulation_rejects_non_integer_a(a):
    with pytest.raises(ValueError, match="a must be an integer"):
        shors_simulation(N=15, a=a)


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"max_attempts": 0}, "max_attempts must be"),
        ({"shots": 0}, "shots must be"),
    ],
)
def test_shors_simulation_rejects_invalid_retry_and_sampling_inputs(kwargs, message):
    with pytest.raises(ValueError, match=message):
        shors_simulation(N=15, a=2, **kwargs)


def test_shors_simulation_returns_structured_success(capsys):
    result = shors_simulation(N=21, a=2, mode="distribution")

    assert result["success"] is True
    assert result["N"] == 21
    assert result["a"] == 2
    assert result["mode"] == "distribution"
    assert result["period"] == 6
    assert set(result["factors"]) == {3, 7}
    assert result["classical_precheck"] is False
    assert len(result["attempts"]) == 1


def test_shors_simulation_returns_structured_classical_precheck(capsys):
    result = shors_simulation(N=22, mode="distribution")

    assert result["success"] is True
    assert result["N"] == 22
    assert result["period"] is None
    assert result["factors"] == (2, 11)
    assert result["classical_precheck"] is True


def test_shors_simulation_returns_structured_retry(capsys):
    result = shors_simulation(N=33, a=2, mode="distribution")

    assert result["success"] is False
    assert result["N"] == 33
    assert result["a"] == 2
    assert result["period"] is None
    assert result["factors"] is None
    assert "Try a different a" in result["message"]


def test_shors_simulation_retries_bases_until_success():
    result = shors_simulation(N=33, max_attempts=4, random_seed=0, mode="distribution")

    assert result["success"] is True
    assert result["factors"] is not None
    assert len(result["attempts"]) >= 1
    assert len(result["attempts"]) <= 4


def test_shors_simulation_supports_sampled_measurements():
    result = shors_simulation(N=21, a=2, mode="distribution", shots=128, random_seed=1)

    assert result["success"] is True
    assert result["shots"] == 128
    assert result["measurement_counts"] is not None
    assert sum(result["measurement_counts"].values()) == 128


def test_sample_measurements_is_seeded_and_normalized():
    probabilities = compute_probs(15, 2, mode="distribution")
    sampled_probabilities, counts = sample_measurements(probabilities, shots=64, random_seed=4)

    assert np.isclose(sampled_probabilities.sum(), 1.0)
    assert sum(counts.values()) == 64


def test_matrix_mode_memory_guard_returns_structured_retry(capsys):
    result = shors_simulation(N=35, a=2, sparse=True, mode="matrix")

    assert result["success"] is False
    assert result["period"] is None
    assert result["factors"] is None
    assert "Use mode='distribution'" in result["message"]


def test_matrix_mode_matches_distribution_mode_for_small_case():
    distribution = compute_probs(15, 2, sparse=True, mode="distribution")
    matrix = compute_probs(15, 2, sparse=True, mode="matrix")

    assert np.isclose(distribution.sum(), 1.0)
    assert np.isclose(matrix.sum(), 1.0)
    assert np.allclose(distribution, matrix)


def test_sparse_oracle_is_a_permutation_matrix_for_small_case():
    oracle = oracle_matrix_sparse(15, 2, first_register_qubits=4, second_register_qubits=4)

    assert np.all(oracle.getnnz(axis=0) == 1)
    assert np.all(oracle.getnnz(axis=1) == 1)


def test_visualization_files_are_created(tmp_path):
    output_dir = str(tmp_path)
    probabilities = compute_probs(15, 2, mode="distribution")

    files = [
        plot_oracle_period_pattern(15, 2, output_dir=output_dir),
        plot_marked_probability_distribution(15, 2, probabilities=probabilities, period=4, output_dir=output_dir),
        plot_matrix_distribution_comparison(15, 2, output_dir=output_dir),
    ]
    diagnostics = plot_continued_fraction_diagnostics(
        15,
        2,
        probabilities=probabilities,
        output_dir=output_dir,
        top_n=6,
    )

    files.extend([diagnostics["plot"], diagnostics["csv"]])

    for path in files:
        assert path
        assert (tmp_path / path.split("/")[-1]).exists()

    assert any(row["accepted"] for row in diagnostics["rows"])


def test_generate_visualization_set_handles_retry_case(tmp_path):
    outputs = generate_visualization_set(33, 2, output_dir=str(tmp_path))

    assert outputs["marked_probabilities"] is None
    assert (tmp_path / "oracle_period_pattern_N=33_a=2.png").exists()
    assert (tmp_path / "continued_fraction_candidates_N=33_a=2.png").exists()
