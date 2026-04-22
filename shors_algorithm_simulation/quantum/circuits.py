from __future__ import annotations

import argparse
import os
from math import ceil, log2, pi
from typing import Any

from shors_algorithm_simulation.plotting.matplotlib_helpers import get_pyplot

try:
    from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
    from qiskit.circuit.gate import Gate

    try:
        from qiskit.circuit.library import QFTGate
    except ImportError:
        QFTGate = None
        from qiskit.circuit.library import QFT
except ImportError as error:
    ClassicalRegister = None
    QuantumCircuit = None
    QuantumRegister = None
    Gate = None
    QFTGate = None
    QFT = None
    QISKIT_IMPORT_ERROR = error
else:
    QISKIT_IMPORT_ERROR = None


def _require_qiskit() -> None:
    """Raise a clear error if optional circuit dependencies are unavailable."""
    if QISKIT_IMPORT_ERROR is not None:
        raise ImportError(
            "Circuit diagram helpers require optional dependencies. "
            "Install them with `pip install .[circuits]` or "
            "`pip install -r requirements-circuits.txt`."
        ) from QISKIT_IMPORT_ERROR


class LabeledBlockGate(Gate if Gate is not None else object):
    """Opaque circuit block used for educational diagrams."""

    def __init__(self, name, num_qubits, label):
        _require_qiskit()
        super().__init__(name, num_qubits, [], label=label)


def register_sizes_from_N(N: int) -> tuple[int, int, int]:
    """Return (n, period_qubits, function_qubits) for the simulator layout."""
    n_qubits = ceil(log2(N))
    return n_qubits, 2 * n_qubits, n_qubits


def inverse_qft_gate(num_qubits: int) -> Any:
    """Return an inverse QFT gate compatible with the installed Qiskit version."""
    _require_qiskit()
    if QFTGate is not None:
        return QFTGate(num_qubits).inverse()
    return QFT(num_qubits, inverse=True)


def build_period_finding_circuit(
    period_qubits: int,
    function_qubits: int,
    oracle_label: str = "Oracle U_a",
    include_measurements: bool = True,
) -> Any:
    """Build the high-level Shor period-finding circuit."""
    _require_qiskit()
    period = QuantumRegister(period_qubits, "|x⟩")
    function = QuantumRegister(function_qubits, "|y⟩")

    if include_measurements:
        measurement = ClassicalRegister(period_qubits, "meas")
        circuit = QuantumCircuit(period, function, measurement)
    else:
        circuit = QuantumCircuit(period, function)

    for qubit in period:
        circuit.h(qubit)

    oracle = LabeledBlockGate("Oracle", period_qubits + function_qubits, oracle_label)
    circuit.append(oracle, list(period) + list(function))
    circuit.append(inverse_qft_gate(period_qubits), period)

    if include_measurements:
        circuit.measure(period, measurement)

    return circuit


def build_matrix_mode_circuit(N: int, a: int, include_measurements: bool = True) -> Any:
    """Build a circuit matching explicit matrix-mode register sizes."""
    _, period_qubits, function_qubits = register_sizes_from_N(N)
    label = f"Matrix oracle U_{a}\n|x⟩|y⟩ → |x⟩|y xor {a}^x mod {N}⟩"
    return build_period_finding_circuit(
        period_qubits,
        function_qubits,
        oracle_label=label,
        include_measurements=include_measurements,
    )


def build_distribution_mode_concept_circuit(
    N: int, a: int, include_measurements: bool = True
) -> Any:
    """
    Build a conceptual diagram for distribution mode.

    Distribution mode does not materialize this circuit. It computes the ideal
    first-register measurement probabilities produced by the same period-finding
    structure.
    """
    _, period_qubits, function_qubits = register_sizes_from_N(N)
    label = f"Analytic periodic groups\nfrom {a}^x mod {N}"
    return build_period_finding_circuit(
        period_qubits,
        function_qubits,
        oracle_label=label,
        include_measurements=include_measurements,
    )


def build_inverse_qft_decomposition_circuit(
    num_qubits: int = 4, include_swaps: bool = True
) -> Any:
    """Build an explicit inverse-QFT gate decomposition."""
    _require_qiskit()
    register = QuantumRegister(num_qubits, "|x⟩")
    circuit = QuantumCircuit(register)

    if include_swaps:
        for index in range(num_qubits // 2):
            circuit.swap(register[index], register[num_qubits - index - 1])
        circuit.barrier()

    for target in range(num_qubits):
        for control in range(target):
            angle = -pi / (2 ** (target - control))
            circuit.cp(angle, register[control], register[target])
        circuit.h(register[target])
        circuit.barrier()

    return circuit


def build_explicit_oracle_decomposition_circuit(
    N: int = 15, a: int = 2, exponent_qubits: int = 2
) -> Any:
    """
    Build a tiny explicit XOR-oracle decomposition using multi-controlled X gates.

    This is intended for small educational diagrams. It implements
    |x⟩|y⟩ -> |x⟩|y xor (a^x mod N)⟩ over the displayed x values.
    """
    _require_qiskit()
    function_qubits = ceil(log2(N))
    exponent = QuantumRegister(exponent_qubits, "|x⟩")
    function = QuantumRegister(function_qubits, "|y⟩")
    circuit = QuantumCircuit(exponent, function)

    controls = list(exponent)
    for x_value in range(2**exponent_qubits):
        oracle_value = pow(a, x_value, N)
        zero_controls = [
            bit_index
            for bit_index in range(exponent_qubits)
            if ((x_value >> bit_index) & 1) == 0
        ]

        for bit_index in zero_controls:
            circuit.x(exponent[bit_index])

        for output_bit in range(function_qubits):
            if (oracle_value >> output_bit) & 1:
                circuit.mcx(controls, function[output_bit])

        for bit_index in reversed(zero_controls):
            circuit.x(exponent[bit_index])

        circuit.barrier()

    return circuit


def draw_circuit(circuit: Any, output_file: str) -> str:
    """Draw a circuit to a PNG file and return the output path."""
    get_pyplot()
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    figure = circuit.draw(output="mpl", filename=output_file)

    if hasattr(figure, "clf"):
        figure.clf()

    return output_file


def draw_circuit_diagrams(
    N: int = 15,
    a: int = 2,
    output_dir: str = "images",
    include_measurements: bool = True,
) -> dict[str, object]:
    """Generate the standard educational circuit diagram set."""
    n_qubits, period_qubits, function_qubits = register_sizes_from_N(N)
    outputs = {}

    high_level = build_period_finding_circuit(
        period_qubits,
        function_qubits,
        oracle_label="Oracle U_a\nencodes a^x mod N",
        include_measurements=include_measurements,
    )
    outputs["high_level"] = draw_circuit(
        high_level,
        os.path.join(output_dir, f"period_finding_circuit_N={N}_a={a}.png"),
    )

    iqft = build_inverse_qft_decomposition_circuit(num_qubits=min(period_qubits, 4))
    outputs["inverse_qft"] = draw_circuit(
        iqft,
        os.path.join(
            output_dir, f"inverse_qft_decomposition_{min(period_qubits, 4)}_qubits.png"
        ),
    )

    toy_exponent_qubits = min(n_qubits, 2)
    oracle = build_explicit_oracle_decomposition_circuit(
        N=N, a=a, exponent_qubits=toy_exponent_qubits
    )
    outputs["explicit_oracle"] = draw_circuit(
        oracle,
        os.path.join(
            output_dir,
            f"oracle_decomposition_N={N}_a={a}_xqubits={toy_exponent_qubits}.png",
        ),
    )

    outputs["registers"] = {
        "n": n_qubits,
        "period_qubits": period_qubits,
        "function_qubits": function_qubits,
        "total_qubits": period_qubits + function_qubits,
    }
    return outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Qiskit circuit diagrams for Shor period finding."
    )
    parser.add_argument("--N", type=int, default=15, help="Integer being factored.")
    parser.add_argument(
        "--a", type=int, default=2, help="Base for modular exponentiation."
    )
    parser.add_argument(
        "--output-dir", default="images", help="Directory for generated PNG files."
    )
    parser.add_argument(
        "--no-measurements",
        action="store_true",
        help="Draw circuits without final measurement operations.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    outputs = draw_circuit_diagrams(
        N=args.N,
        a=args.a,
        output_dir=args.output_dir,
        include_measurements=not args.no_measurements,
    )

    registers = outputs.pop("registers")
    print(
        "Registers: "
        f"period={registers['period_qubits']}, "
        f"function={registers['function_qubits']}, "
        f"total={registers['total_qubits']}"
    )
    for name, path in outputs.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
