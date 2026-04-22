import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.quantum_part.circuit_diagrams import draw_circuit, build_period_finding_circuit


if __name__ == "__main__":
    circuit = build_period_finding_circuit(
        period_qubits=4,
        function_qubits=4,
        oracle_label="Oracle U\n|x⟩|y⟩ → |x⟩|y xor f(x)⟩",
    )
    draw_circuit(circuit, "images/quantum_circuit.png")
