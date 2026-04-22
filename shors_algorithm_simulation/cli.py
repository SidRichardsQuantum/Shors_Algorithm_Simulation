from __future__ import annotations

import argparse
import json

from shors_algorithm_simulation.core import ShorsResult, json_ready, shors_simulation
from shors_algorithm_simulation.plotting.probabilities import plot_probs
from shors_algorithm_simulation.probabilities import compute_probs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Classically simulate Shor's period-finding algorithm."
    )
    parser.add_argument("--N", type=int, default=15, help="Integer to factor.")
    parser.add_argument(
        "--a", type=int, default=None, help="Base for modular exponentiation."
    )
    parser.add_argument(
        "--mode",
        choices=["distribution", "matrix"],
        default="distribution",
        help="Period-finding simulation mode.",
    )
    parser.add_argument(
        "--dense",
        action="store_true",
        help="Use dense matrices in matrix mode. Sparse matrices are used by default.",
    )
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=1,
        help="Number of bases to try when --a is omitted.",
    )
    parser.add_argument(
        "--shots",
        type=int,
        default=None,
        help="Sample this many first-register measurements instead of using exact probabilities.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Seed for deterministic base selection and measurement sampling.",
    )
    parser.add_argument(
        "--plots",
        action="store_true",
        help="Save the first-register probability plot.",
    )
    parser.add_argument(
        "--output-dir",
        default="images",
        help="Directory for generated plots.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the structured result as JSON after the human-readable output.",
    )
    return parser.parse_args()


def print_human_result(result: ShorsResult) -> None:
    print(f"N = {result['N']}")
    for index, attempt in enumerate(result["attempts"], start=1):
        print(f"Attempt {index}: a = {attempt['a']}")
        print(attempt["message"])
        if attempt["shots"] is not None:
            distinct = len(attempt["measurement_counts"] or {})
            print(
                f"Sampled measurements: shots={attempt['shots']}, distinct outcomes={distinct}"
            )
        if index != len(result["attempts"]):
            print("-" * 40)


def save_probability_plot(result: ShorsResult, sparse: bool, output_dir: str) -> None:
    a = result["a"]
    if a is None or result["classical_precheck"]:
        return

    probabilities = compute_probs(result["N"], a, sparse=sparse, mode=result["mode"])
    if result["measurement_counts"] is not None and result["shots"] is not None:
        probabilities = probabilities * 0
        for outcome, count in result["measurement_counts"].items():
            probabilities[outcome] = count / result["shots"]

    plot_probs(result["N"], a, probabilities, show_plots=True, output_dir=output_dir)


def main() -> int:
    args = parse_args()
    result = shors_simulation(
        N=args.N,
        a=args.a,
        sparse=not args.dense,
        mode=args.mode,
        max_attempts=args.max_attempts,
        shots=args.shots,
        random_seed=args.seed,
    )

    print_human_result(result)

    if args.plots:
        save_probability_plot(result, sparse=not args.dense, output_dir=args.output_dir)

    if args.json:
        print(json.dumps(json_ready(result), indent=2))

    return 0 if result["success"] else 1
