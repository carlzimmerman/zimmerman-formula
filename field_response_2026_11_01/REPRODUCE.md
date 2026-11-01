# Reproduce FR01

The package is self-contained apart from the recorded Python/NumPy/SciPy
installation and the mathbox bounded runner. Inputs under `inputs/` are copies
of the exact earlier sources, so no uncommitted earlier lane is required.
Tested versions: Python 3.9.6, NumPy 1.26.2, SciPy 1.11.4 on macOS.

From the repository root, with the installed skill path substituted:

```bash
python3 field_response_2026_11_01/reproduce.py radial \
  --runner /path/to/computation-audit/scripts/run_experiment.py \
  --output field_response_2026_11_01/reproduction_radial_001
```

Named lanes are `radial`, `kinetic`, `canonical-energy`, `static`,
`static-refinement`, `dilute-stability`, `dilute-static`, `endpoints`, and
`checks`. Give each a fresh output directory. The wrapper uses fixed reviewed
scripts and their declared inputs, sets the same short numerical resource caps,
and refuses to overwrite evidence. It installs nothing and starts no background
or production simulation. NumPy/SciPy are in the observed user-site installation;
Python `-I` excludes them here and is not the recorded successful command.

Each run writes a v2 manifest plus stdout/stderr and its declared result files.
The original exact argv and before/after hashes remain in each saved manifest.
The current static lanes intentionally return nonzero when any requested branch
does not converge. Read their per-state checks and coverage; do not relabel a
partially completed grid as a complete physical pass.

Validate a new manifest with:

```bash
python3 /path/to/computation-audit/scripts/validate_manifest.py \
  field_response_2026_11_01/reproduction_radial_001/manifest.json \
  --root "$PWD"
```

Local implementation controls:

```bash
python3 field_response_2026_11_01/test_controls.py
python3 field_response_2026_11_01/test_kinetic_control.py
```

`checks` audits the published result files, including their exact rational
global map-admissibility bounds. The canonical-energy and endpoint lanes
reconstruct frozen witnesses/endpoints from the included original result files;
they deliberately do not replace those inputs with a newly tuned result.

The initial import, serialization and control-truncation failures are retained
under their original run names and source hashes. Do not overwrite them or
refresh historical hashes. Documentary clarifications are explicit in
DIAGNOSTIC_DICTIONARY.md and KINETIC_METADATA_CLARIFICATION.md.
