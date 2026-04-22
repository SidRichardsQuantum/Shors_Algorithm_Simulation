from __future__ import annotations

import os

import numpy as np

from shors_algorithm_simulation.plotting.formatting import set_ket_xticks
from shors_algorithm_simulation.plotting.matplotlib_helpers import get_pyplot


def plot_probs(
    N: int,
    a: int,
    prob_first_register: np.ndarray,
    show_plots: bool = True,
    output_dir: str = "images",
) -> None:
    """Plot first-register probabilities that were already computed."""
    plt = get_pyplot()
    Q = len(prob_first_register)
    tick_step = max(1, Q // 16)

    plt.figure(figsize=(10, 6))
    plt.bar(range(Q), prob_first_register, alpha=0.7, color="lightcoral", edgecolor="darkred")
    plt.xlabel("First Register State")
    plt.ylabel("Probability")
    plt.title(f"First Register Measurement Probabilities\n(Period detection for N={N}, a={a})")
    plt.grid(True, alpha=0.3)
    axis = plt.gca()
    set_ket_xticks(axis, range(0, Q, tick_step))
    plt.tight_layout()
    print("-" * 40)

    if show_plots:
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"first_register_probabilities_N={N}_a={a}.png")
        plt.savefig(output_file, dpi=300, bbox_inches="tight")
        print(f"\nPlot saved as: {output_file}")

    plt.close()
