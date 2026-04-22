import argparse
import json
from math import gcd
from src.classical_parts.pre_checks import pre_checks
from src.plots_and_period.find_period import find_period
from src.classical_parts.post_checks import post_checks
from src.plots_and_period.probability_plot import plot_probs


def shors_simulation(N=15, a=None, show_plots=True, sparse=True, mode="distribution"):
    """
    Shor's algorithm simulation.
    Default: N = 15

    Args:
        N: Integer to factor
        a: Base for modular exponentiation. If None, will be chosen randomly.
           Must be between 2 and N-1 (inclusive).
        mode: "distribution" computes the period-finding probabilities directly.
              "matrix" explicitly applies the simulated gate matrices.
    """

    # Validate a if provided
    if a is not None:
        if not (2 <= a <= N - 1):
            raise ValueError(f"Invalid value for 'a': {a}. Must be between 2 and {N - 1} (inclusive).")

    # Classical preprocessing
    print(f"N = {N}\nRunning Classical Checks...")
    success, value, message = pre_checks(N, a)
    print(message)

    if success is True:
        # Classical checks found factors
        factors = tuple(int(factor) for factor in value)
        return _build_result(
            success=True,
            N=N,
            a=a,
            mode=mode,
            factors=factors,
            period=None,
            message=message,
            classical_precheck=True,
        )

    else:
        # Classical checks passed, proceed to the quantum part
        print("Proceeding to quantum algorithm...")

        # 'value' from pre_checks is now the 'a' that was used
        a = value

        # Run the algorithm
        try:
            r, probabilities = find_period(N, a, sparse=sparse, mode=mode)
        except (ValueError, MemoryError) as error:
            print(error)
            return _build_result(
                success=False,
                N=N,
                a=a,
                mode=mode,
                factors=None,
                period=None,
                message=str(error),
                classical_precheck=False,
            )

        # Do the factorization
        result = post_checks(N, a, r)
        print(result)

        # Now show the plot
        plot_probs(N, a, probabilities, show_plots=show_plots, sparse=sparse)

        factors = _factors_from_period(N, a, r)
        return _build_result(
            success=factors is not None,
            N=N,
            a=a,
            mode=mode,
            factors=factors,
            period=r,
            message=result,
            classical_precheck=False,
        )


def _build_result(success, N, a, mode, factors, period, message, classical_precheck):
    """Return a stable programmatic result while examples continue printing output."""
    return {
        "success": success,
        "N": N,
        "a": a,
        "mode": mode,
        "period": period,
        "factors": factors,
        "message": message,
        "classical_precheck": classical_precheck,
    }


def _factors_from_period(N, a, r):
    """Recover non-trivial factors from a validated period."""
    if r is None or r % 2 != 0:
        return None

    half_power = pow(a, r // 2, N)
    factor1 = gcd(half_power + 1, N)
    factor2 = gcd(half_power - 1, N)

    if 1 < factor1 < N and 1 < factor2 < N and factor1 * factor2 == N:
        return (factor1, factor2)

    return None


def _json_ready(result):
    """Convert tuple values to lists for JSON output."""
    cleaned = dict(result)
    if isinstance(cleaned.get("factors"), tuple):
        cleaned["factors"] = list(cleaned["factors"])
    return cleaned


def parse_args():
    parser = argparse.ArgumentParser(description="Classically simulate Shor's period-finding algorithm.")
    parser.add_argument("--N", type=int, default=15, help="Integer to factor.")
    parser.add_argument("--a", type=int, default=None, help="Base for modular exponentiation.")
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
        "--plots",
        action="store_true",
        help="Save the first-register probability plot.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the structured result as JSON after the human-readable output.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    result = shors_simulation(
        N=args.N,
        a=args.a,
        show_plots=args.plots,
        sparse=not args.dense,
        mode=args.mode,
    )

    if args.json:
        print(json.dumps(_json_ready(result), indent=2))

    return 0 if result["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
