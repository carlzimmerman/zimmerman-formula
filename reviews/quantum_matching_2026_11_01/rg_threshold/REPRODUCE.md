# TP02 reproduction

All executed source inputs are frozen. Results are not written over an old
run directory. The records use the installed mathbox computation-audit
runner and validator, not bundled project copies. Author versions:
Python3.9.6, NumPy1.26.2, SciPy1.11.4, SymPy1.14.0, mpmath1.3.0 as listed
per manifest. No new packages, random sampling or downloaded files are used.

`reproduce.py` accepts a stage and a fresh direct-child output directory.
Stages are cs, interface, pressure01, pressure03, pressure05, pressure1,
relaxation and relaxed_pressure. For example from the repository root:

```bash
python3 reviews/quantum_matching_2026_11_01/rg_threshold/reproduce.py pressure03 run_pressure03_repeat --runner /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py
```

The helper runs the authored command and its frozen contract into the new
folder. It never executes a command read from an evidence manifest. The
relaxed-pressure and interface stages use the original frozen control
results as their stated comparison inputs. Repeating the same code is a
reproducibility check, not independent mathematical validation.

Validate a retained record against current file hashes:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py reviews/quantum_matching_2026_11_01/rg_threshold/run_pressure_03/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

On this macOS machine CPU affinity and the requested address-space limit
are unavailable. Runs use one numerical thread and supported wall/CPU/log
caps, with observed peak RSS recorded. No unimplemented cap is claimed.

`improved.py` exposes evaluate/profile for high-precision U and RG-only
angular F in reference X0 coordinates. `relaxation.py` exposes the full
normal tadpoles and Hessian. Its float64 spectral derivatives must be
field-differentiated with finite, repeated stencils; mpmath infinitesimal
differences through those float64 values would be invalid. The native
phase grand-potential implementation is owned by matter_coupling/.
