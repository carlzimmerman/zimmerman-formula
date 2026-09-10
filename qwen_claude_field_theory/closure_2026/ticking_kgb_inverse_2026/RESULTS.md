# Execution checkpoint

Authoritative evidence: `run_002/manifest.json`, validated with input/output
hash checking against the repository. Overall runner exit: **0**. This records
successful execution, NOT a complete theory.

## Exact new files

All paths below are relative to
`qwen_claude_field_theory/closure_2026/ticking_kgb_inverse_2026/`:

- `kgb_inverse.py`
- `mond_profile.py`
- `test_kgb.py`
- `KGBFormal.lean`
- `run_suite.py`
- `audit_contract.json`
- `SOURCES.md`
- `REPORT.md`
- `RESULTS.md`
- `run_001/manifest.json`
- `run_001/stdout.txt`
- `run_001/stderr.txt`
- `run_002/manifest.json`
- `run_002/stdout.txt`
- `run_002/stderr.txt`

No existing source files were intentionally changed. The earlier run is
retained with its original provenance; it predates the report's clarification
that the Einstein coupling has not been identified with measured Newton G.
Use `run_002`, not the superseded report hash in `run_001`.

## Commands and important exits

Commands below run from this package unless noted. Full absolute argv and
working directories, including every nested historical test command, appear
in `run_002/stdout.txt`. Resource-runner argv/inputs/caps are recorded in the
manifest and contract.

| Command | Exit | Meaning |
|---|---:|---|
| `python3 -B kgb_inverse.py` | 0 | Symbolic variation, inverse, halo and FLRW identities verified |
| `python3 -B kgb_inverse.py --require-closure` | 2 | Explicitly refuses full-theory certification |
| `python3 -B mond_profile.py` | 0 | 16 inverse samples and two-mass comparison executed; health/compatibility FAIL |
| `python3 -B -m unittest -v test_kgb.py` | 0 | Nine new regression checks passed |
| `lake env lean ../../ticking_kgb_inverse_2026/KGBFormal.lean` | 0 | Three conditional theorems checked; run from the existing Lean project |
| `python3 -B run_suite.py` in `../linear_curvature_clock_2026` | 0 | Forty earlier regression tests and their audits executed as expected |
| `python3 -B run_suite.py` in this package | 0 | All six top-level execution statuses matched their documented meanings |

Lean project working directory:
`qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026`.
Lean printed only `propext`, `Classical.choice`, `Quot.sound` dependencies for
the three new theorems; no `sorryAx`. Total unit tests: **49**.

From the repository root, the actual evidence validation command was:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/ticking_kgb_inverse_2026/run_002/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

It exited **0**: valid evidence record; mathematical interpretation still
requires review. The test-first general-inverse check initially failed with
a missing `general_inverse` result, then passed after implementation. The
canonical scalar principal-symbol benchmark passed independently.

## Research result

Strongest constructive result: an explicitly varied ticking KGB action has an
exact positive-density flat halo and an expanding homogeneous branch, with
the derived local scalar cones healthy in their stated parameter ranges.

Strongest obstruction: the fixed power fixes the halo speed; the preferred
exponential, zero-radial-pressure inverse instead loses scalar health and
gives incompatible G_X values at a shared X for the two tested normalizations.

Status: **OPEN research route; no complete MOND theory, no empirical
confirmation, no coefficient derivation.** The next calculation is the shared
two-function inverse across masses, allowing radial pressure while enforcing
stability. See `REPORT.md` for assumptions, equations, exclusions and credit.
