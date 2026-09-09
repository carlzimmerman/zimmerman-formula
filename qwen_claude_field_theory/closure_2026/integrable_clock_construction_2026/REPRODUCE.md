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

## IC6 strong continuation and IC7 isotropic action repair

Base `0b75e72bf5797e451beb258847ade528cd9c4551`, 2026-09-08. This section
supersedes the previous checkpoint's open-work list, not its immutable runs.
The current action is [IC7_CURVATURE_SQUARE.md](IC7_CURVATURE_SQUARE.md).
IC6's stronger auxiliary/Dirac and characteristic results are retained under
their own action ID. **The full theory is OPEN; both revisions fail the
requested all-background propagation requirement.**

### Exact files created or changed

All names below are relative to this directory unless specified.

New scientific programs, all executed, each with its executed test module:

- `ic6_strong_auxiliary.py`, `test_ic6_strong_auxiliary.py`;
- `ic6_dirac_flow.py`, `test_ic6_dirac_flow.py`;
- `ic6_odd_characteristics.py`, `test_ic6_odd_characteristics.py`;
- `ic6_even_characteristics.py`, `test_ic6_even_characteristics.py`;
- `ic7_curvature_square.py`, `test_ic7_curvature_square.py`.

New mathematical documents: `IC6_STRONG_AUXILIARY.md`, `IC6_DIRAC_FLOW.md`,
`IC6_ODD_CHARACTERISTICS.md`, `IC6_EVEN_CHARACTERISTICS.md`,
`IC6_CONTINUATION_REVIEW.md`, `IC7_CURVATURE_SQUARE.md`.
New provenance: `continuation_contract.json` and
`continuation_run_001/run_index.json`. Each of the following twelve fresh
subdirectories under `continuation_run_001/` contains exactly
`manifest.json`, `stdout.txt`, `stderr.txt`:

    strong, odd, flow, even, repair,
    strong_required, odd_required, flow_required, even_required,
    repair_required, tests, closure_tests.

Existing files changed: this `REPRODUCE.md` and
`../CRISPY_FRIED_CHICKEN_RECIPE.md` (current construction pointer; existing
NavierStokesAndEuler inspiration/citation retained). Frozen prior scientific
files and prior recorded evidence are unchanged. Unrelated dirty G03, hunt,
website and other files are excluded from this checkpoint.

### Exact commands and observed exits

The complete executed runner argv, child argv, validator argv, child and
wrapper exits and runtimes are in
[continuation_run_001/run_index.json](continuation_run_001/run_index.json).
The runner uses the actual Python 3.13.9, SymPy 1.13.1, NumPy 1.26.4,
SciPy 1.14.1 and mpmath 1.3.0 environment. Each run has a 180-second wall
limit, 1 MiB combined-output limit and one cooperative numerical-library
thread. No memory/affinity or interval-arithmetic guarantee is claimed.
The manifest pins all declared code, imports, action documents and contract.

Scientific commands executed from the repository root (the bounded runner
sets the cooperative thread environment for its children):

```bash
python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic6_strong_auxiliary.py
python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic6_odd_characteristics.py
python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic6_dirac_flow.py
python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic6_even_characteristics.py
python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic7_curvature_square.py
python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic6_strong_auxiliary.py --require-full-theory
python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic6_odd_characteristics.py --require-all-background-causality
python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic6_dirac_flow.py --require-field-closure
python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic6_even_characteristics.py --require-all-background-causality
python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic7_curvature_square.py --require-full-closure
python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026 -p 'test_*.py' -v
python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026 -p 'test_*.py' -v
git diff --check
```

| Important check | Observed result | Child exit |
| --- | --- | --- |
| Five default mathematical programs | Derivations/checks reported at stated scope | 0 each |
| IC7 exact symbolic bridge groups | Twelve zero residuals, including actual witness jets | 0 |
| Complete construction suite | 176 tests passed; 59.714 seconds inside test process | 0 |
| Existing lapse/closure regression suite | 32 tests passed; 2.347 seconds | 0 |
| Five demanding theory/causality/closure gates | Unpassed; no full certificate | 2 each |
| Twelve manifest validators with current-root hash checks | Valid reproducibility records, not mathematical certificates | 0 each |
| Patch whitespace | No errors | 0 |

The five failed scientific gates have wrapper exit1 and retained manifest
status `failed`; this is not converted into a physics PASS. The bounded
construction-suite runtime including process overhead was 60.071979 seconds.
An earlier direct full-suite run also passed 176 tests (57.879 seconds).
Test-first IC7 execution failed on the missing implementation (exit1), then
11 tests passed; the singular-static cutoff added two more passing tests.
IC6 strong development exposed a structural-expression comparison issue,
resolved with an exact zero-difference check. IC6 even development replaced
an over-tight finite-k leading-term comparison with its derived next terms.
These development failures are not claimed as physical counterexamples.

### Strongest mathematical result and next unavoidable calculation

IC6 now has a strong local nonlinear auxiliary solve in specified Sobolev
spaces and an explicit smooth-domain Dirac multiplier construction. Its
unprojected homogeneous trajectory preserves the auxiliary constraints under
step refinement. A symmetry-decoupled odd tensor has the physical null
principal cone in the specified anisotropic plane class. These are scoped
results, not coupled inhomogeneous existence or a full physical DOF theorem.

The complete even reduction, independently bridged to its compact action,
proves S4'(1)<0 on the actual nearby isotropic IC6 branch. IC7 then adds the
explicit curvature-square coefficient c7=theta*v^T M^(-1)v/8, with smooth
zero extension before any singular inverse. Direct variation cancels the
isotropic quartic coefficient identically on eta=theta=1, preserves the
flat homogeneous equations and exact witness quadratic action, and gives
positive sampled scalar/tensor masses and bounded sampled high-frequency
wave ratios. No coefficients are fitted to the desired speeds.

The sheared-background mixing is still nonzero. The next action construction
must simultaneously satisfy N2=N2^T and C4−B2 A0^(-1)B2^T=0 there, then
derive the remaining k² cones including actual background time derivatives.
This is the next necessary calculation, not a claim that it will complete
the theory. Galactic matching, measured G, full PPN, exact zero-field control,
coupled causal evolution and realistic cosmology remain required afterward.
Mathbox auditing led to the explicit domain cutoff and the refusal to promote
bounded computations to full closure. Lean/lake were unavailable on PATH;
no Lean build, novelty proof or empirical test is claimed.

## IC8–IC10: optical alignment and a local clock plateau, 2026-09-08

Current result: [IC10_LOCAL_CLOCK.md](IC10_LOCAL_CLOCK.md), preceded by
[OPTICAL_ALIGNMENT.md](OPTICAL_ALIGNMENT.md). Full theory **OPEN**.
Scientific starting revision `0aa6e0cef`; the live checkout also acquired
Fable commits `0e20cf937`, `aea949c58` and `9727a5083` during this work.
Their histories and findings were inspected; L4's independent IC7 script
was actually rerun. Its strict two-total-mode gate exits2 while its numerical
reproduction checks pass. Fable's newer cluster claims are not adopted as
universal screening no-go theorems or as empirical evidence for IC10.

### Exact files created/changed

New files in this directory:

- `ic8_shear_integrability.py`, `test_ic8_shear_integrability.py`;
- `ic9_lightcone_alignment.py`, `test_ic9_lightcone_alignment.py`;
- `ic10_local_clock.py`, `test_ic10_local_clock.py`;
- `OPTICAL_ALIGNMENT.md`, `IC10_LOCAL_CLOCK.md`, `IC10_REVIEW.md`;
- `optical_contract.json`, `optical_run_001/run_index.json`.

Each of the eight new directories below `optical_run_001/` contains exactly
`manifest.json`, `stdout.txt`, `stderr.txt`:

    ic8, ic9, ic10, ic8_required, ic9_required, ic10_required,
    tests, closure_tests.

Changed existing files: this reproduction record and
`../CRISPY_FRIED_CHICKEN_RECIPE.md` (current pointer only). Its existing
NavierStokesAndEuler attribution is retained. No prior frozen scientific
file, prior manifest, or unrelated dirty file is changed by this checkpoint.

### Exact commands and observed exits

The complete executed runner argv is factored without omission into common
prefix and per-run suffix arrays in
[optical_run_001/run_index.json](optical_run_001/run_index.json). The index
also records exact child and validator argv, child/wrapper exits and elapsed
times. Each run pins its inputs and actual Git revision/dirty observation.

Scientific commands, executed from the repository root:

```bash
python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic8_shear_integrability.py
python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic9_lightcone_alignment.py
python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic10_local_clock.py
python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic8_shear_integrability.py --require-full-closure
python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic9_lightcone_alignment.py --require-full-closure
python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic10_local_clock.py --require-full-closure
python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026 -p 'test_*.py' -v
python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026 -p 'test_*.py' -v
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python -B fable_independent_2026/L4_verify_ic7.py
git diff --check
```

The recorded runner sets one cooperative numerical-library thread per child,
180-second wall and 1MiB combined-log bounds. No memory/affinity guarantee
or interval-arithmetic certificate is implied. All eight manifest validators
were executed with `--root` and exited0, including the failed full-goal runs.

| Important check | Result | Child exit |
| --- | --- | --- |
| IC8, IC9, IC10 default programs | Scoped derivations retained | 0 each |
| Complete construction suite | 202 tests passed, 72.339 seconds | 0 |
| Existing closure regression | 32 tests passed, 2.855 seconds | 0 |
| Three full-theory gates | Incomplete requirements retained | 2 each |
| Independent IC10 review | 7 tests; exact/numerical corroboration | 0 |
| Fable L4 rerun | Numerical reproduction passes; strict mode gate fails | 2 |
| All eight provenance validators | Current input/output hashes valid | 0 each |
| Patch whitespace | No errors | 0 |

The three strict gates have wrapper exit1 and manifest status `failed`.
A valid failed-run record is not a physics PASS. A prior direct construction
run also passed all 202 tests in 68.821 seconds. All three new scientific
scripts and all three new test modules were executed. Development red/green
tests and numerical-method corrections are recorded in the index.

### Strongest result and exact next gate

IC9's optical coordinate removes the tested shear/curvature obstruction
and aligns its tensor cone, but its finite-wave scalar remains rational.
The potential-only local-kinetic trial retains a nonzero pole residue.
IC10 changes the trace kinetic term too: on eta=1, exact variation yields
Einstein gravity plus the explicit local pressure P(Xtilde,w) constructed
from the original U. Its regular vacuum auxiliary is algebraic; the clock
is a separately identified propagating mode, not hidden as an auxiliary.
Fresh background solves, actual fixed-momentum constraint brackets and
finite homogeneous evolution pass the stated positive-energy and
subluminality tests. Physical expansion is about 0.08216 e-folds over the
tested interval—not a complete or realistic cosmology.

The next boundary is now located on that actual solution:
S=0.230723991364998, r²=5/4, cs²=0.242306706149330. The unavoidable next
calculation is the **full phase-action evolution and characteristics across
that boundary**, retaining eta derivatives. Neither the vacuum pressure nor
the plateau count may be extrapolated through it. Galactic AQUAL, independent
Phi/Psi, all PPN parameters, measured G, matter-coupled health, strong coupling
and y=0/global-k=0 control remain open afterward.

[The independent IC10 review](IC10_REVIEW.md) records the frozen input hashes,
separate-runtime checks and their precise scope. Mathbox auditing prompted
the exact finite-wave calculation, the fixed-canonical-momentum bracket,
the separate homogeneous evolution and the refusal to promote a local
construction to full closure. Lean/lake were unavailable on PATH; no Lean
proof, new empirical prediction or global novelty certification is claimed.
