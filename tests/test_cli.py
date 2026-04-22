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


def test_main_cli_uses_requested_output_dir(tmp_path):
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
            "--plots",
            "--output-dir",
            str(tmp_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    output_file = tmp_path / "first_register_probabilities_N=15_a=2.png"
    assert str(output_file) in result.stdout
    assert output_file.exists()


def test_main_cli_supports_sampled_measurements():
    result = subprocess.run(
        [
            sys.executable,
            "main.py",
            "--N",
            "21",
            "--a",
            "2",
            "--shots",
            "128",
            "--seed",
            "1",
            "--json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "Sampled measurements: shots=128" in result.stdout
    assert '"shots": 128' in result.stdout
    assert '"measurement_counts"' in result.stdout


def test_visualization_cli_selects_oracle_plot(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "examples.visualizations_example",
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


def test_shots_sweep_example_creates_outputs(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "examples.shots_sweep_example",
            "--N",
            "21",
            "--a",
            "2",
            "--shots",
            "16",
            "32",
            "--trials",
            "3",
            "--seed",
            "1",
            "--output-dir",
            str(tmp_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "shots=16:" in result.stdout
    assert (tmp_path / "shots_sweep_N=21_a=2_trials=3.csv").exists()
    assert (tmp_path / "shots_sweep_N=21_a=2_trials=3.png").exists()
