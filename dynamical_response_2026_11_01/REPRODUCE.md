# Reproducing DR01

Use Python 3.9.6, NumPy 1.26.2 and SciPy 1.11.4 (the recorded environment).
Matplotlib 3.9.4 is used only for the standalone result plot. No package install
is performed. Run commands from the repository root; choose a fresh label.

The wrapper uses the installed computation-audit runner at the SKILL path
specified at the top of reproduce_v3.py. On another machine, change that
path in a new local wrapper copy to the installed runner location. That helper
records the command, versions, current Git revision/dirty state, immutable
input hashes before and after, resource limits, exit status and output hashes.
It does not turn successful execution into a mathematical proof.

```sh
python3 dynamical_response_2026_11_01/reproduce_v3.py my_orbit_check --kind benchmark
python3 dynamical_response_2026_11_01/reproduce_v3.py my_independent_check --kind review
python3 dynamical_response_2026_11_01/reproduce_v3.py my_baseline --state baseline --level 2 --nbasis 12 --krylov 1152
python3 dynamical_response_2026_11_01/reproduce_v3.py my_compact --state compact --level 2 --nbasis 24 --nphase 2048 --nharm 32 --krylov 1152
python3 dynamical_response_2026_11_01/reproduce_v3.py my_free_check --kind bare_exact
python3 dynamical_response_2026_11_01/test_controls_v2.py
```

The exact bare check compares independently computed final spectral energy
and angular momentum with the shipped baseline_bare_001 and compact_bare_001
records at their original identical grids. It does not silently compare to
newly named runs. To create a new bare halo response, add --bare to a response
command. All reported results are linear coefficients at the explicit forcing
normalization, not finite-amplitude simulations of a stellar bar.

Each science command produces result.json and response_series.npz in its fresh
run directory. Series rows are time, external power, torque, real/imaginary
quadrupole, and real/imaginary core-restricted quadrupole. Keys ending _late
contain time and real/imaginary post-pulse quadrupole. The latter are retained
diagnostics and are not established damping curves.

## Version and failure provenance

response.py and reproduce.py are frozen first-run sources. response_v2.py
fixes the zero-feedback rank-zero control and rescales a diagnostic residual;
it retains the same dressed equations. reproduce_v2.py is the historical
wrapper. Its unused --kind review path has the wrong output argument and an
incomplete dependency list; use reproduce_v3.py, which fixes that orchestration
and pins both explicit amendment files.

independent_checks_001 deliberately remains a failed reference-check record.
Its direct IVP conserved state accurately but lost relative accuracy in tiny
off-resonant accumulated work. The separate normalized reference integration
in independent_checks_002 passes the original gates. Read
INDEPENDENT_CONTROL_AMENDMENT_A1.md; no physical result was retuned.

For a manifest, run the installed helper as:

```sh
python3 /path/to/computation-audit/scripts/validate_manifest.py dynamical_response_2026_11_01/RUN/manifest.json --root "$PWD"
```

Each run was capped at 1800 seconds or less and one numerical-library thread.
Inputs copied from FR01 live under inputs/fr01. The current evolving shared
repository is not consulted to refresh those inputs.
