import subprocess
import sys


def test_main_cli_json_success():
    result = subprocess.run(
        [
            sys.executable,
            "main.py",
            "--N",
            "15",
            "--a",
            "2",
            "--mode",
            "distribution",
            "--json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert '"success": true' in result.stdout
    assert '"period": 4' in result.stdout


def test_visualization_cli_selects_oracle_plot(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "examples/visualizations_example.py",
            "--N",
            "15",
            "--a",
            "2",
            "--plots",
            "oracle",
            "--output-dir",
            str(tmp_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "oracle:" in result.stdout
    assert (tmp_path / "oracle_period_pattern_N=15_a=2.png").exists()
