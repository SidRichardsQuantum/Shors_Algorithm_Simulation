from __future__ import annotations

import csv
import os
from math import ceil, log2

import numpy as np

from shors_algorithm_simulation.period import find_period, period_candidate_diagnostics
from shors_algorithm_simulation.plotting.formatting import ket_label, set_ket_xticks
from shors_algorithm_simulation.plotting.matplotlib_helpers import get_pyplot
from shors_algorithm_simulation.probabilities import compute_probs


def multiplicative_order(N: int, a: int) -> int | None:
    """Return the classical order of a mod N for diagnostics."""
    value = 1
    for r in range(1, N + 1):
        value = (value * a) % N
        if value == 1:
            return r
    return None


def plot_oracle_period_pattern(
    N: int,
    a: int,
    output_dir: str = "images",
    max_points: int | None = None,
) -> str:
    """Plot x -> a^x mod N to show the hidden periodicity."""
    plt = get_pyplot()
    os.makedirs(output_dir, exist_ok=True)

    Q = 2 ** (2 * ceil(log2(N)))
    points = max_points or min(Q, max(32, 4 * N))
    x_values = np.arange(points)
    y_values = np.array([pow(a, int(x), N) for x in x_values])
    order = multiplicative_order(N, a)

    plt.figure(figsize=(10, 5))
    plt.plot(x_values, y_values, marker="o", linewidth=1.5, markersize=4)
    if order:
        for x in range(order, points, order):
            plt.axvline(x, color="0.7", linestyle="--", linewidth=1)
    tick_step = max(1, points // 16)
    set_ket_xticks(plt.gca(), range(0, points, tick_step))
    plt.xlabel("Input State")
    plt.ylabel("a^x mod N")
    plt.title(f"Oracle Period Pattern for N={N}, a={a}")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_file = os.path.join(output_dir, f"oracle_period_pattern_N={N}_a={a}.png")
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()
    return output_file


def plot_marked_probability_distribution(
    N: int,
    a: int,
    probabilities: np.ndarray | None = None,
    period: int | None = None,
    output_dir: str = "images",
    mode: str = "distribution",
) -> str:
    """Plot first-register probabilities with expected peak markers for a recovered period."""
    plt = get_pyplot()
    os.makedirs(output_dir, exist_ok=True)

    probabilities = probabilities if probabilities is not None else compute_probs(N, a, mode=mode)
    if period is None:
        period, _ = find_period(N, a, mode=mode)

    Q = len(probabilities)
    tick_step = max(1, Q // 16)
    expected_peaks = [round(s * Q / period) for s in range(period) if round(s * Q / period) < Q]

    plt.figure(figsize=(11, 6))
    plt.bar(range(Q), probabilities, alpha=0.65, color="lightcoral", edgecolor="darkred")
    for peak in expected_peaks:
        plt.axvline(peak, color="navy", linestyle="--", linewidth=1, alpha=0.75)
    plt.xlabel("First Register State")
    plt.ylabel("Probability")
    plt.title(f"First Register Probabilities with Period Markers (N={N}, a={a}, r={period})")
    set_ket_xticks(plt.gca(), range(0, Q, tick_step))
    plt.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()

    output_file = os.path.join(output_dir, f"marked_probabilities_N={N}_a={a}_r={period}.png")
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()
    return output_file


def plot_continued_fraction_diagnostics(
    N: int,
    a: int,
    probabilities: np.ndarray | None = None,
    output_dir: str = "images",
    top_n: int = 12,
    mode: str = "distribution",
) -> dict[str, object]:
    """Save a continued-fraction candidate CSV and a compact candidate plot."""
    plt = get_pyplot()
    os.makedirs(output_dir, exist_ok=True)

    probabilities = probabilities if probabilities is not None else compute_probs(N, a, mode=mode)
    rows = period_candidate_diagnostics(N, a, probabilities, top_n=top_n)

    csv_file = os.path.join(output_dir, f"continued_fraction_candidates_N={N}_a={a}.csv")
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "measured_value",
                "probability",
                "fraction",
                "denominator",
                "tested_periods",
                "valid_periods",
                "accepted",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "measured_value": row["measured_value"],
                    "probability": row["probability"],
                    "fraction": f"{row['fraction'].numerator}/{row['fraction'].denominator}",
                    "denominator": row["denominator"],
                    "tested_periods": " ".join(str(r) for r in row["tested_periods"]),
                    "valid_periods": " ".join(str(r) for r in row["valid_periods"]),
                    "accepted": row["accepted"],
                }
            )

    plot_rows = sorted(rows, key=lambda row: row["measured_value"])
    labels = [ket_label(row["measured_value"]) for row in plot_rows]
    probabilities_for_plot = [row["probability"] for row in plot_rows]
    colors = ["seagreen" if row["accepted"] else "steelblue" for row in plot_rows]

    plt.figure(figsize=(11, 6))
    plt.bar(labels, probabilities_for_plot, color=colors, alpha=0.8)
    plt.xlabel("Measured First-Register State")
    plt.ylabel("Probability")
    plt.title(f"Continued-Fraction Candidate Measurements (N={N}, a={a})")
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()

    plot_file = os.path.join(output_dir, f"continued_fraction_candidates_N={N}_a={a}.png")
    plt.savefig(plot_file, dpi=300, bbox_inches="tight")
    plt.close()
    return {"plot": plot_file, "csv": csv_file, "rows": rows}


def plot_matrix_distribution_comparison(
    N: int,
    a: int,
    output_dir: str = "images",
    sparse: bool = True,
) -> str:
    """Overlay matrix and distribution mode probabilities for a small case."""
    plt = get_pyplot()
    os.makedirs(output_dir, exist_ok=True)

    distribution = compute_probs(N, a, sparse=sparse, mode="distribution")
    matrix = compute_probs(N, a, sparse=sparse, mode="matrix")
    difference = matrix - distribution
    x_values = np.arange(len(distribution))

    fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=True)
    axes[0].plot(x_values, distribution, label="distribution", linewidth=2)
    axes[0].plot(x_values, matrix, label="matrix", linestyle="--", linewidth=2)
    axes[0].set_ylabel("Probability")
    axes[0].set_title(f"Matrix vs Distribution Mode (N={N}, a={a})")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].bar(x_values, difference, color="slategray")
    axes[1].set_xlabel("First Register State")
    axes[1].set_ylabel("Matrix - distribution")
    axes[1].grid(True, axis="y", alpha=0.3)
    tick_step = max(1, len(distribution) // 16)
    set_ket_xticks(axes[1], range(0, len(distribution), tick_step), rotation=45, ha="right")
    fig.tight_layout()

    output_file = os.path.join(output_dir, f"matrix_vs_distribution_N={N}_a={a}.png")
    fig.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return output_file


def generate_visualization_set(
    N: int,
    a: int,
    output_dir: str = "images",
    mode: str = "distribution",
) -> dict[str, object]:
    """Generate the main educational visualization set for one input."""
    probabilities = compute_probs(N, a, mode=mode)
    outputs = {
        "oracle_pattern": plot_oracle_period_pattern(N, a, output_dir=output_dir),
        "continued_fraction": plot_continued_fraction_diagnostics(
            N,
            a,
            probabilities=probabilities,
            output_dir=output_dir,
            mode=mode,
        ),
    }

    try:
        period, _ = find_period(N, a, mode=mode)
        outputs["marked_probabilities"] = plot_marked_probability_distribution(
            N,
            a,
            probabilities=probabilities,
            period=period,
            output_dir=output_dir,
            mode=mode,
        )
    except ValueError:
        outputs["marked_probabilities"] = None

    return outputs
