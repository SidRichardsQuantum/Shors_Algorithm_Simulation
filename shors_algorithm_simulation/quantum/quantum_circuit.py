from shors_algorithm_simulation.quantum.circuits import (
    build_period_finding_circuit,
    draw_circuit,
)

if __name__ == "__main__":
    circuit = build_period_finding_circuit(
        period_qubits=4,
        function_qubits=4,
        oracle_label="Oracle U\n|x⟩|y⟩ → |x⟩|y xor f(x)⟩",
    )
    draw_circuit(circuit, "images/quantum_circuit.png")
