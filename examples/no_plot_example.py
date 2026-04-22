from shors_algorithm_simulation import shors_simulation

if __name__ == "__main__":
    """Run a deterministic example without opening plots."""
    result = shors_simulation(N=21, a=2, sparse=True, mode="distribution")
    print(f"Structured result: factors={result['factors']}, period={result['period']}")
