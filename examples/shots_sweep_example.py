from __future__ import annotations

import argparse
import csv
import os
from collections.abc import Sequence

from shors_algorithm_simulation import shors_simulation
from shors_algorithm_simulation.plotting.matplotlib_helpers import get_pyplot

DEFAULT_SHOTS = (16, 32, 64, 128, 256, 512, 1024)


def run_shots_sweep(
    N: int = 21,
    a: int = 2,
    shots_values: Sequence[int] = DEFAULT_SHOTS,
    trials: int = 20,
    seed: int = 0,
    output_dir: str = "images",
) -> dict[str, object]:
    """
    Estimate sampled-measurement success rate for a fixed factoring instance.

    Each trial samples a fresh first-register histogram from the ideal
    distribution, then runs continued-fraction period recovery on that histogram.
    """
    os.makedirs(output_dir, exist_ok=True)

    rows = []
    for shots in shots_values:
        successes = 0
        for trial in range(trials):
            result = shors_simulation(N=N, a=a, shots=shots, random_seed=seed + trial)
            successes += int(result["success"])

        success_rate = successes / trials
        row = {
            "N": N,
            "a": a,
            "shots": shots,
            "trials": trials,
            "successes": successes,
            "success_rate": success_rate,
        }
        rows.append(row)
        print(f"shots={shots}: success_rate={success_rate:.3f} ({successes}/{trials})")

    csv_path = os.path.join(output_dir, f"shots_sweep_N={N}_a={a}_trials={trials}.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["N", "a", "shots", "trials", "successes", "success_rate"],
        )
        writer.writeheader()
        writer.writerows(rows)

    plot_path = os.path.join(output_dir, f"shots_sweep_N={N}_a={a}_trials={trials}.png")
    _plot_shots_sweep(rows, plot_path)

    print(f"CSV saved as: {csv_path}")
    print(f"Plot saved as: {plot_path}")
    return {"csv": csv_path, "plot": plot_path, "rows": rows}


def _plot_shots_sweep(rows: list[dict[str, object]], output_file: str) -> None:
    plt = get_pyplot()
    shots = [int(row["shots"]) for row in rows]
    rates = [float(row["success_rate"]) for row in rows]

    plt.figure(figsize=(9, 5))
    plt.plot(shots, rates, marker="o", linewidth=2)
    plt.xscale("log", base=2)
    plt.ylim(-0.05, 1.05)
    plt.xlabel("Shots")
    plt.ylabel("Success Rate")
    plt.title("Sampled Shor Period Recovery Success Rate")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot sampled-measurement success rate versus shots."
    )
    parser.add_argument(
        "--N", type=int, default=21, help="Composite integer to factor."
    )
    parser.add_argument(
        "--a", type=int, default=2, help="Base for modular exponentiation."
    )
    parser.add_argument(
        "--shots",
        nargs="+",
        type=int,
        default=list(DEFAULT_SHOTS),
        help="Shot counts to test.",
    )
    parser.add_argument("--trials", type=int, default=20, help="Trials per shot count.")
    parser.add_argument(
        "--seed",
        type=int,
        default=0,
        help="Base random seed for reproducible sampling.",
    )
    parser.add_argument(
        "--output-dir", default="images", help="Directory for generated CSV and plot."
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_shots_sweep(
        N=args.N,
        a=args.a,
        shots_values=args.shots,
        trials=args.trials,
        seed=args.seed,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()
