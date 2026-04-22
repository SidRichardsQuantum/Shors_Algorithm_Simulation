import argparse

from shors_algorithm_simulation.period import find_period
from shors_algorithm_simulation.probabilities import compute_probs
from shors_algorithm_simulation.plotting.diagnostics import (
    plot_continued_fraction_diagnostics,
    plot_marked_probability_distribution,
    plot_matrix_distribution_comparison,
    plot_oracle_period_pattern,
)


PLOT_CHOICES = ["oracle", "marked", "continued", "comparison", "all"]


def parse_args():
    parser = argparse.ArgumentParser(description="Generate Shor period-finding visualizations.")
    parser.add_argument("--N", type=int, default=21, help="Semiprime for oracle/probability/candidate plots.")
    parser.add_argument("--a", type=int, default=2, help="Base for oracle/probability/candidate plots.")
    parser.add_argument(
        "--mode",
        choices=["distribution", "matrix"],
        default="distribution",
        help="Mode used for probability-based plots.",
    )
    parser.add_argument(
        "--plots",
        nargs="+",
        choices=PLOT_CHOICES,
        default=["all"],
        help="Plots to generate.",
    )
    parser.add_argument("--output-dir", default="images", help="Directory for generated plots and CSV files.")
    parser.add_argument("--top-n", type=int, default=12, help="Number of continued-fraction candidates to plot.")
    parser.add_argument("--comparison-N", type=int, default=15, help="N for matrix/distribution comparison.")
    parser.add_argument("--comparison-a", type=int, default=2, help="a for matrix/distribution comparison.")
    parser.add_argument("--dense-comparison", action="store_true", help="Use dense matrices for comparison plot.")
    return parser.parse_args()


def selected_plots(plot_args):
    requested = set(plot_args)
    if "all" in requested:
        return {"oracle", "marked", "continued", "comparison"}
    return requested


def print_output(name, value):
    if isinstance(value, dict):
        print(f"{name}: plot={value['plot']}, csv={value['csv']}, rows={len(value['rows'])}")
    else:
        print(f"{name}: {value}")


def main():
    args = parse_args()
    plots = selected_plots(args.plots)
    outputs = {}
    probabilities = None

    if {"marked", "continued"} & plots:
        probabilities = compute_probs(args.N, args.a, mode=args.mode)

    if "oracle" in plots:
        outputs["oracle"] = plot_oracle_period_pattern(args.N, args.a, output_dir=args.output_dir)

    if "continued" in plots:
        outputs["continued"] = plot_continued_fraction_diagnostics(
            args.N,
            args.a,
            probabilities=probabilities,
            output_dir=args.output_dir,
            top_n=args.top_n,
            mode=args.mode,
        )

    if "marked" in plots:
        try:
            period, _ = find_period(args.N, args.a, mode=args.mode)
            outputs["marked"] = plot_marked_probability_distribution(
                args.N,
                args.a,
                probabilities=probabilities,
                period=period,
                output_dir=args.output_dir,
                mode=args.mode,
            )
        except ValueError as error:
            outputs["marked"] = f"skipped ({error})"

    if "comparison" in plots:
        outputs["comparison"] = plot_matrix_distribution_comparison(
            args.comparison_N,
            args.comparison_a,
            output_dir=args.output_dir,
            sparse=not args.dense_comparison,
        )

    for name, value in outputs.items():
        print_output(name, value)


if __name__ == "__main__":
    main()
