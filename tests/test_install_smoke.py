import os
import subprocess
import sys
import venv
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_editable_install_exposes_console_script(tmp_path):
    venv_dir = tmp_path / "venv"
    venv.EnvBuilder(with_pip=True, system_site_packages=True).create(venv_dir)

    bin_dir = "Scripts" if os.name == "nt" else "bin"
    python = venv_dir / bin_dir / ("python.exe" if os.name == "nt" else "python")
    shors_sim = (
        venv_dir / bin_dir / ("shors-sim.exe" if os.name == "nt" else "shors-sim")
    )

    subprocess.run(
        [
            str(python),
            "-m",
            "pip",
            "install",
            "--no-deps",
            "--no-build-isolation",
            "-e",
            str(REPO_ROOT),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    result = subprocess.run(
        [str(shors_sim), "--N", "15", "--a", "2", "--mode", "distribution", "--json"],
        check=True,
        capture_output=True,
        cwd=tmp_path,
        text=True,
    )

    assert '"success": true' in result.stdout
    assert '"period": 4' in result.stdout


def test_circuit_helpers_import_without_qiskit_and_fail_clearly():
    code = """
import importlib.abc
import sys


class BlockQiskit(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "qiskit" or fullname.startswith("qiskit."):
            raise ImportError("qiskit intentionally blocked")
        return None


sys.meta_path.insert(0, BlockQiskit())

from shors_algorithm_simulation.quantum.circuits import build_period_finding_circuit, register_sizes_from_N

assert register_sizes_from_N(15) == (4, 8, 4)

try:
    build_period_finding_circuit(1, 1)
except ImportError as error:
    assert "pip install .[circuits]" in str(error)
else:
    raise AssertionError("Expected optional dependency ImportError")
"""

    subprocess.run(
        [sys.executable, "-c", code],
        check=True,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
