# Changelog

All notable changes to this project are documented here.

## v0.1.1, 06/05/2026

### Added

- Added README badges for PyPI version, supported Python version, tests, docs, license, and GitHub Sponsors.
- Added PyPI-facing project metadata, keywords, classifiers, and project URLs in `pyproject.toml`.

### Changed

- Updated README command-line examples to prefer the installed `shors-sim` console entry point.
- Updated the README project structure to include current packaging, plotting, and circuit helper files.
- Updated the generated documentation homepage action to point to installation guidance before the PyPI release is live.
- Expanded `.gitignore` coverage for common Python build, coverage, and test artifacts.

### Fixed

- Replaced the PyPI-derived Python versions badge with a static `>=3.10` badge so README previews do not show a missing badge before publishing.
- Removed the deprecated license classifier from `pyproject.toml` to keep package builds compatible with modern setuptools license metadata validation.

## v0.1.0, 22/04/2026

### Added

- Added a real installable package, `shors_algorithm_simulation`, with a typed public API.
- Added the `shors-sim` console entry point.
- Added sampled-measurement support with `shots` and deterministic `random_seed`.
- Added retry orchestration with `max_attempts` when no base `a` is provided.
- Added optional circuit dependencies via `.[circuits]` and `requirements-circuits.txt`.
- Added package metadata in `pyproject.toml`.
- Added GitHub Actions CI for Python 3.10, 3.11, 3.12, circuit extras, and package build smoke tests.
- Added a PyPI trusted-publishing workflow for GitHub Releases.
- Added package install smoke tests.
- Added `examples/shots_sweep_example.py` for success rate versus sampled measurements.
- Added configurable output directories for generated plots.
- Added `MANIFEST.in` so source distributions include docs, examples, tests, and reference outputs.
- Added `.gitattributes` for consistent line endings and binary/reference artifact handling.

### Changed

- Replaced the public `src.*` import namespace with `shors_algorithm_simulation.*`.
- Moved CLI parsing and human-readable output into `shors_algorithm_simulation.cli`.
- Split algorithm, probability, validation, plotting, and quantum helper code into separate modules.
- Moved probability sampling into `shors_algorithm_simulation.probabilities`.
- Moved period finding into `shors_algorithm_simulation.period`.
- Moved classical checks into `shors_algorithm_simulation.validation`.
- Updated examples to run as modules with `python -m examples...`.
- Updated documentation to clarify that distribution mode and shot sampling use ideal simulated probabilities.

### Removed

- Removed the old tracked `src/` Python package modules.
- Removed Qiskit and pylatexenc from the core requirements file.
- Removed `sys.path.append(...)` setup from examples.

## Earlier History

- Added educational circuit diagrams and circuit documentation.
- Added distribution mode for faster ideal first-register probability simulation.
- Added matrix mode comparisons, runtime examples, diagnostic plots, and regression tests.
