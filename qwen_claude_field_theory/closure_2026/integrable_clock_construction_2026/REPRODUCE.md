# Reproduce IC-1 construction checkpoint

Run from the repository root. Runtime: Python 3.13.9 (Anaconda), SymPy 1.13.1,
NumPy 1.26.4. No network or empirical data are used by these calculations.

## Exact scientific commands executed

```bash
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026 -p 'test_*.py' -v
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/integrable_clock.py
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/integrable_clock.py --require-full-closure
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026 -p 'test_*.py' -v
git diff --check
```

| Check | Observed result | Exit |
| --- | --- | --- |
| New computation tests, final run | 9 passed | 0 |
| Construction derivation (recorded runner below) | Exact residuals zero; computed rank6 kinetic block, rank4 homogeneous constraints; OPEN | 0 |
| Full-goal reporting gate | Missing proof obligations retained; **not a certificate** | 2 |
| Relevant existing lapse/primary closure tests | 32 passed | 0 |
| Patch whitespace | Clean | 0 |

Development test-first runs failed intentionally before implementation: five
missing derivation tests, then two missing family/spatial functions, then one
missing Ward function. Each exited1; the implemented final suite exits0.
These were missing-code checks, not physical counterexamples. An intermediate
six-test and an eight-test suite also passed. All newly created scientific
scripts were executed.

## Pinned run

This exact argv was executed using the installed computation-audit runner:

```bash
python -B /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/contract.json --input qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ACTION.md --input qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/integrable_clock.py --input qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/test_integrable_clock.py --output qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/run_001 --timeout 60 --max-output-bytes 1048576 --max-threads 1 -- python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/integrable_clock.py
python -B /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Both exited0. The manifest pins the actual base commit, dirty-state observation,
input hashes, command, software, limits and stdout/stderr. Use a **new output
directory** for a new recorded run; do not overwrite run_001. On another machine,
resolve its installed runner and project-root paths before reproducing.
Library thread caps are cooperative, not a hardware-resource guarantee.

Read-only independent review of module SHA256
`c6a5b227aed84fa53829659327ef986c2fc813a4888455515da52d651322cce3`
recomputed the primary bracket and homogeneous PB determinant relation and
reran tests/default CLI/reporting gate: exits0/0/2. No blocker was found within
the report's deliberately limited claims; full-field obligations remain open.

## Files in this checkpoint

New: ACTION.md, REPORT.md, REPRODUCE.md, contract.json, integrable_clock.py,
test_integrable_clock.py, run_001/manifest.json, run_001/stdout.txt,
run_001/stderr.txt. Existing file changed: ../CRISPY_FRIED_CHICKEN_RECIPE.md
(current-candidate link only). No prior scientific code or dirty G03 work changed.

The strongest result is the exact canonical integrability identity plus an
expanding, regular, positive-homogeneous-kinetic branch of the same action.
Full theory: **OPEN**. Next calculation: inhomogeneous scalar reduction and
the secondary functional constraint operator on that exact background.

## IC-2 continuation at base 6dd851cf5

New files: IC2_ACTION.md, SCALAR_REPORT.md, scalar_completion.py,
test_scalar_completion.py, scalar_contract.json, scalar_run_001/manifest.json,
scalar_run_001/stdout.txt, scalar_run_001/stderr.txt. Updated existing files:
REPORT.md (follow-up scope correction), REPRODUCE.md (this record), and
../CRISPY_FRIED_CHICKEN_RECIPE.md (current IC-2 pointer). IC-1's scientific
code, tests, ACTION.md and run_001 remain byte-for-byte unchanged.

Additional exact commands executed:

```bash
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026 -p 'test_*.py' -v
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/scalar_completion.py --require-all-wavelength-frequency
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/scalar_completion.py --require-full-closure
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026 -p 'test_*.py' -v
python -B /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/scalar_contract.json --input qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ACTION.md --input qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/IC2_ACTION.md --input qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/integrable_clock.py --input qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/scalar_completion.py --input qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/test_scalar_completion.py --output qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/scalar_run_001 --timeout 60 --max-output-bytes 1048576 --max-threads 1 -- python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/scalar_completion.py
python -B /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/scalar_run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Final observations: 20 construction/scalar tests pass, exit0; 32 existing
closure tests pass, exit0; recorded scalar calculation has 27 zero exact
residuals, exit0. All-wavelength-frequency and full-closure flags both exit2.
A development run was interrupted with Ctrl-C (exit130) while an algebraic
logarithm-normalization bug was being corrected; its output is not evidence
for the final claims. Final tests and CLI runs use the frozen corrected file.

Two separate read-only derivations checked the critical coefficients. The
reviewed final scalar module SHA256 is
`801e50f8a3485842eec9bafd58d4f652c42200050917da6d9f0360aea5ff7745`;
test module SHA256 is
`60b4f075b1d520729d8ea9a9c34ea87c92ee8754ab331d89ae14bd4b825c560f`.

Current result: **IC-2 OPEN**, with an explicit all-x-positive quadratic
kinetic coefficient and UV physical scalar speed squared 4/9 on the exact
expanding branch. The finite negative-frequency band, physical causal support,
nonlinear closure and full PPN are not certified. See SCALAR_REPORT.md for
the exact next calculations. The full objective has not been marked complete.

## IC-4 construction continuation at base 0a9f9fa33

Current action: [IC4_ACTION.md](IC4_ACTION.md). Mathematical result and limits:
[LOCAL_WAVE_REPORT.md](LOCAL_WAVE_REPORT.md). Earlier sections above are
historical run records for different action revisions, not extra IC-4 passes.

New scientific code and tests, all executed:

- `clock_locality_completion.py`, `test_clock_locality_completion.py`:
  intermediate IC-3 coefficient matching, with its remaining pole retained.
- `ir_growth.py`, `test_ir_growth.py`, `IR_GROWTH.md`:
  independent IC-2 finite-band future bound; not used to certify IC-4.
- `curvature_operator_bridge.py`, `test_curvature_operator_bridge.py`:
  full physical-density variation and independently reduced new coupling.
- `local_clock_wave.py`, `test_local_clock_wave.py`:
  explicit IC-4 construction, energy and compact packet identities, numerical
  transfer with refinement and independent analytic controls.
- `quadratic_dirac.py`, `test_quadratic_dirac.py`:
  independently restored spatial gauge, Hamiltonian, actual Poisson matrices,
  preservation and counts for IC-2, IC-4 and the separate genuine zero mode.

New prose/contracts: `IC4_ACTION.md`, `LOCAL_WAVE_REPORT.md`,
`ir_contract.json`, `wave_contract.json`. New recorded evidence:

- `ir_run_001/manifest.json`, `stdout.txt`, `stderr.txt`, `run_index.json`;
  `ir_run_001/full_closure/` and `ir_run_001/tests/` each contain
  `manifest.json`, `stdout.txt`, `stderr.txt`.
- `wave_run_001/run_index.json`; each of `wave_run_001/wave/`,
  `bridge/`, `dirac/`, `matching/`, `tests/` contains
  `manifest.json`, `stdout.txt`, `stderr.txt`.

Existing files updated: this `REPRODUCE.md` and
`../CRISPY_FRIED_CHICKEN_RECIPE.md` (current construction pointer only).
Frozen IC-1/IC-2 scientific code, tests, action descriptions and old evidence
remain unchanged; unrelated dirty G03 and other work is not included.

### Executed commands and exits

Run from the repository root. The primary run uses Anaconda Python 3.13.9,
SymPy 1.13.1, NumPy 1.26.4, SciPy 1.14.1, mpmath 1.3.0.

```bash
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026 -p 'test_*.py' -v
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026 -p 'test_*.py' -v
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/local_clock_wave.py
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/local_clock_wave.py --require-full-closure
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/curvature_operator_bridge.py
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/clock_locality_completion.py
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/quadratic_dirac.py --require-full-nonlinear-count
git diff --check
```

The full exact bounded-run commands, including every input path, runner
location, limits, outputs and validators, are retained in
[wave_run_001/run_index.json](wave_run_001/run_index.json).
This records executed commands, not an unexecuted suggested plan. The primary
scientific calculations and the complete construction test suite each have a
fresh manifest. All five manifests were validated with `--root`.

| Important check | Actual result | Exit |
| --- | --- | --- |
| Complete construction tests | 73 passed; 15.594 seconds in the recorded run | 0 |
| Existing lapse/closure regression tests | 32 passed | 0 |
| IC-4 default calculation | 29 zero exact residuals; positive kinetic; numerical controls passed | 0 |
| Independent curvature bridge | 38 zero exact residuals | 0 |
| Actual quadratic Dirac calculation | 78 checked identities/sign checks; pinned inputs match | 0 |
| Intermediate IC-3 matching | Derived coefficients; remaining pole explicitly reported | 0 |
| IC-4 full-theory requirement | Still unproved; not a successful closure test | 2 |
| Full nonlinear Dirac requirement | Still unproved | 2 |
| Five primary provenance validators | Input/output hashes verified, not mathematical certification | 0 each |
| Whitespace check | Clean | 0 |

The separate [IR run index](ir_run_001/run_index.json) records exact commands
using Python 3.9.6, SymPy 1.14.0, NumPy 1.26.2 and SciPy 1.11.4: nine tests
exit0, default calculation exit0, full-closure child exit2. The last is
authentically recorded by its runner as `failed`, runner exit1; all three
manifests validate with exit0. Their inputs are still byte-identical. The
primary 73-test run also reproduces the IR checks under the Anaconda runtime.

New scripts were written tests-first. Root's initial local-wave tests failed
with exit1 for the missing implementation; the later packet test failed with
exit1 for the absent reconstruction, then all eleven passed. A concurrently
developed Dirac source pin detected a changed IC-4 input, refused it, and was
explicitly re-audited/repinned after the source froze. This development event
is not a physical counterexample. One documentation patch failed to match
context and was reapplied correctly; it changed no scientific output.

### Independent review and current limits

An independent physical-metric variation verified the factor $16\ell^2/3$;
an independent raw-action solve and a separate Hamiltonian route recovered
the same scalar equation and readouts. The latter does not borrow IC-2's
Poisson rank: IC-4's secondary bracket and determinant are computed anew.
The shared upstream background remains a common dependency, not an
independently formalized theorem.

Read-only proof review confirmed the compact-packet cone argument only for
the stated data class, and corrected the prose distinction between $P$ and
the original trace momentum $P-18z$. It also clarified the squared-speed
parameter and the static zero-field notation. The final report retains
harmonic-moment restrictions and the lack of an IR-uniform canonical norm.

Frozen key hashes:

- `local_clock_wave.py`: `a88d84135ea99263c62ecc339feffc76830623fb70b394222a1843174be7511d`
- `test_local_clock_wave.py`: `d03571c74dc9327bcfc5aea883aae19d3f50a10d21bb2fabe4c5e96e99bf3d21`
- `curvature_operator_bridge.py`: `a7e0f9985911a34dbac3e87c3460e9332bb918d46cbbfc47266a00f748b31864`
- `quadratic_dirac.py`: `8c5476ac217df3f3b146f7293ff69e91d4e72e8c4665e1ebfc2fd26fde98a1e0`

Strongest result: one explicit correction constructs an all-wave-number healthy
linear scalar wave on the exact expanding branch, together with computed
quadratic constraint closure and restricted finite-speed physical packets.
Full theory: **OPEN**. Next: nonlinear functional constraint preservation and
admissible-data correspondence, followed by the same action's galactic/FLRW
matching and PPN. No empirical, Lean, global novelty or final-theory claim is made.

## 2026-09-08: nonlinear Hamiltonian, auxiliary square, and IC-6 tensor balance

Base `6708f1e3e695a99f3fc3f121e14528f68ace641c`. This is a later construction
checkpoint, not a reinterpretation of the preceding frozen IC-4 evidence.
The preceding turn only verified the blueprint; this turn changes the actual
action and derives its connected comparisons.

### Files and exact executed commands

New scientific files in this directory:

- `nonlinear_hamiltonian.py`, `test_nonlinear_hamiltonian.py`, `NONLINEAR_HAMILTONIAN.md`.
- `nonlinear_auxiliary_symbol.py`, `test_nonlinear_auxiliary_symbol.py`, `AUXILIARY_SYMBOL.md`.
- `nonlinear_square_completion.py`, `test_nonlinear_square_completion.py`, `IC5_ACTION.md`,
  `NONLINEAR_SQUARE_REPORT.md`, `NONLINEAR_COMPLETION_REVIEW.md`.
- `tensor_balance_completion.py`, `test_tensor_balance_completion.py`, `TENSOR_BALANCE.md`.
- `nonlinear_contract.json`; `nonlinear_run_001/run_index.json`; the nine
  `nonlinear_run_001/{hamiltonian,symbol,square,tensor,tests,hamiltonian_required,symbol_required,square_required,tensor_required}`
  subdirectories, each containing `manifest.json`, `stdout.txt`, `stderr.txt`.

Only this reproduction file and the recipe's current-checkpoint pointer are
edited among pre-existing tracked files. All previously pinned calculation
and action files remain unchanged; unrelated dirty work is preserved.

[The executed run index](nonlinear_run_001/run_index.json) contains every
exact primary and strict-gate runner argument, input path, child exit,
wrapper exit, runtime, output locator and validator command. All nine runs
pin the same 32 declared inputs. The commands actually executed by their
children, from the repository root, were `python -B` followed by the
directory prefix `qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/`
and each of:

```text
nonlinear_hamiltonian.py
nonlinear_auxiliary_symbol.py
nonlinear_square_completion.py
tensor_balance_completion.py
nonlinear_hamiltonian.py --require-functional-closure
nonlinear_auxiliary_symbol.py --require-full-nonlinear-closure
nonlinear_square_completion.py --symbolic-only --require-full-closure
tensor_balance_completion.py --symbolic-only --require-all-background-causality
```

The full test command was:

```text
python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026 -p 'test*.py'
```

The existing regression command, separately executed, was:

```text
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026 -p 'test*.py'
```

Recorded runtime: Python 3.13.9, SymPy 1.13.1, NumPy 1.26.4; existing
SciPy 1.14.1 and mpmath 1.3.0 remain dependencies of the regression suite.
The bounded runner used 180 seconds per job, a 1 MiB log cap and one
cooperative numerical-library thread. Independent jobs ran in parallel.
No operating-system memory or affinity limit is claimed.

### Important results and exits

| Check | Actual result | Child exit |
| --- | --- | --- |
| Full construction suite | 121 passed, 58.717 seconds | 0 |
| Existing lapse/closure suite | 32 passed, 2.397 seconds | 0 |
| IC-4 full metric Legendre/auxiliary identities | 28 exact checks; source pin matches | 0 |
| IC-4 auxiliary-symbol computation | 21 exact residual groups vanish | 0 |
| IC-5 explicit nonlinear square construction | Exact bridges and separate 16/32/64-grid solves pass | 0 |
| IC-6 tensor balance and nonlinear momentum elimination | 28 exact residual groups; its own grid solves pass | 0 |
| IC-4 full functional closure requested | Not established | 2 |
| IC-4 symbol/full nonlinear closure requested | Not established | 2 |
| IC-5 full theory requested | Not established | 2 |
| IC-6 all-background causality requested | Not established | 2 |
| Nine provenance validators with `--root` | Hash/input checks pass; not proof certification | 0 each |
| `git diff --check` | No whitespace errors | 0 |

The four strict-gate runs have wrapper exit 1 and manifest status `failed`
because their children correctly return 2. They are retained as unpassed
requirements, not relabeled successful closure checks. All newly created
scientific and test scripts were executed.

Tests-first development exposed missing implementations before code was
added. Root also fixed three return-key mismatches and replaced structural
SymPy expression comparison with a zero-difference check. A generic-function
second derivative retained dummy mixed-derivative substitutions; the test
was implemented with unrestricted second jets, for which the same local
identity is exact. The momentum-even activation and supplied-density solver
each received a failing behavior test before implementation. None of these
development errors is reported as a physical obstruction.

### Strongest mathematical result and next calculation

IC-6 has an explicit covariant phase action and a compact nonlinear
Lagrangian on its regular plateau. Its exact auxiliary square admits a
derived local weak-operator coercivity estimate; the stationary equations,
flat isotropic homogeneous Hamiltonian and IC-4 witness quadratic sector
have checked same-action bridges. The corrected action derives
`K_T=G_T=J_T>0`, hence physical `c_T=c`, on flat homogeneous isotropic
backgrounds beyond the special `F=0` witness. Its own nonlinear grid solves
reach maximum residual `1.2568062232542204e-13`, with decreasing refinement
differences. This is not empirical validation.

Independent mathematical review confirmed the covariant normalization,
momentum elimination, mixed-space coercivity and tensor balance. It required
an explicit common-domain qualifier for the full Dirac-block inverse and
an explicit static boundary prescription; both are included. The tensor
review covers both polarizations by isotropy, not arbitrary inhomogeneous
or anisotropic backgrounds. Agreement of reviewers is not a formal certificate.

**Full theory: OPEN.** The next unavoidable calculation is the coupled
inhomogeneous physical characteristic system and complete IC-6 multiplier
drift, including domains of the secondary Poisson bracket. Establishing a
weak auxiliary inverse does not by itself exclude instantaneous physical
response or prove regular evolution. Then the same theory must meet galactic
matching, full PPN, zero-field control and realistic cosmology. The original
thirteen requirements are unchanged. No global novelty claim, empirical fit,
first-principles a0-Lambda derivation, or project-specific Lean certificate is
made; Mathlib's coercivity theorem was source-checked as a possible later
formalization dependency, not executed here.
