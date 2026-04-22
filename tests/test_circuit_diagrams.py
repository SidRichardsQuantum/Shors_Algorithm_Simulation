import subprocess
import sys

import pytest

pytest.importorskip("qiskit")

from shors_algorithm_simulation.quantum.circuits import draw_circuit_diagrams


def test_draw_circuit_diagrams_creates_png_files(tmp_path):
    outputs = draw_circuit_diagrams(N=15, a=2, output_dir=str(tmp_path))

    assert outputs["registers"]["period_qubits"] == 8
    assert outputs["registers"]["function_qubits"] == 4
    assert outputs["registers"]["total_qubits"] == 12

    for key in ["high_level", "inverse_qft", "explicit_oracle"]:
        path = tmp_path / outputs[key].split("/")[-1]
        assert path.exists()
        assert path.stat().st_size > 0


def test_circuit_diagram_cli_creates_requested_output(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "examples.circuit_diagrams_example",
            "--N",
            "15",
            "--a",
            "2",
            "--output-dir",
            str(tmp_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "Registers: period=8, function=4, total=12" in result.stdout
    assert (tmp_path / "period_finding_circuit_N=15_a=2.png").exists()
