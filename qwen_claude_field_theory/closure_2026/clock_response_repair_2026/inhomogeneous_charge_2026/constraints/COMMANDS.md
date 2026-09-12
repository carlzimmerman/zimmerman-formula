# Commands and provenance

Working directory: `/Users/carlzimmerman/new_physics/zimmerman-formula`.
Only `inhomogeneous_charge_2026/constraints/` was written by this subtask.
No original source edits or Git mutations were performed. The bounded runner
reads Git metadata to record actual revision and dirty state.

Final executed commands, both exit 0:

```bash
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/inhomogeneous_charge_2026/constraints -p 'test_*.py' -v
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/inhomogeneous_charge_2026/constraints/run_bounded.py
```

The final five-test run passed in .963 seconds. The wrapper records its full
argv, runs the installed computation-audit bounded runner, and validates the
resulting manifest against current inputs. Experiment exit 0 and validation
exit 0. The computation runtime was 4.031907 seconds, starting
2026-09-12T16:10:36.113046Z, with a 120-second wall cap and 1 MiB combined log
cap. The one-thread numerical setting is cooperative; no hard memory,
CPU-time or affinity cap is asserted.

The software versions were read from the executing environment: Python3.9.6,
SymPy1.14.0, NumPy1.26.2, SciPy1.11.4. No randomness is used.

Archive:

- `run_001/result.json`: exact expressions/checks, three sets of 101 slice
  points, actual lapse and evolution jets, principal coefficients, charge
  density, box charge and endpoint fluxes, and independent numerical checks.
- `run_001/manifest.json`: actual source revision, dirty state, source hashes
  before/after, argv, software, bounds, runtime, exit and result hash.
- `run_001/stdout.txt` and `stderr.txt`: process logs.

Selected SHA-256 hashes:

| File | SHA-256 |
|---|---|
| plane_slice.py | eb4a7ea239a36f7c1e757b3161f3977bd8fdcfd92b040be7b499ca10a44d3676 |
| test_plane_slice.py | 99f3fd2d45e8425953c8b701ea6b47e9a87dd83ce8f08158b202aae24f4a2f4c |
| run_001/result.json | d69d6aa6f361f29a652915c9284cf0cc8f175bf1a7eb0ae69d8f9496afdc99e7 |

Earlier direct runs used the same script command with result paths
`exploratory.json`, `refined_exploratory.json`, and `charge_exploratory.json`;
each exited 0. These are retained transient development snapshots, not final
validated evidence. The first predates the independent Ricci/time checks and
the reflected-gradient principal-frame correction for negative b. The second
adds those checks; the third adds charge but predates endpoint-flux output.
The final run supersedes all three. Initial four-test and later five-test
suites passed; no failing experiment was discarded or relabeled as success.
A read-only `sed` command to a guessed `nonlinear_evolution/constitutive.py`
path exited1; the correct authoritative `nonlinear_evolution_2026/` path was
then read and used. This was a path-discovery failure, not a physical result.

In the result, `max_residuals` orders Hamiltonian, momentum, clock, debraided
scalar, clock preservation, and direct-curvature scalar. The first five
include equations used to solve unknowns, so independent finite-difference
and direct-curvature checks must accompany their interpretation.
The imported principal function's `quarter_gamma0` label means before its
explicit cubic corrections at fixed passed jets; these passed jets already
contain the source action's gamma-dependent coefficients. Use
`quarter_finite_gamma` for the complete reported principal diagnostic.

No global charge normalization or exterior matching is encoded in the input
contract. Passing manifest validation establishes provenance, not a theorem.

Final mathematical self-review clarified two notational shorthands in the
report only: B is the Lorentzian Hessian trace, and the volume measure uses
sqrt(det h_ij), not the transverse extrinsic-curvature variable h. No source
equation or numerical artifact changed. Two attempted report patches were
rejected because of unrelated unmatched context; the corrected report-only
patch then applied. These editing failures did not modify evidence.
