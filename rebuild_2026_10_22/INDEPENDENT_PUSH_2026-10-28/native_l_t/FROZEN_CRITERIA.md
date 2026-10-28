# Native L / T audit: frozen finite contract

Written 2026-10-28 before executing this audit's new arithmetic. This lane is an independent, bounded audit of NL1 and
the claim that an NL1 pass would leave only kappa fitted. Existing NL1, X48, CL2, CL3 and LEE1 files are read only.
The coordinator explicitly prohibited commits and restricted new files to this directory; those instructions supersede
the older lane briefs' commit and destination rules. No jobs are started, interrupted or duplicated.

## Assertion tested

1. The committed ng48 A2 JSON's three concentration medians can be recomputed from its `ok`, `ng == 48` records.
2. The documented NL1 synthetic NFW `c=4`, N=12000, RNG seed 1 benchmark passes its 15% tolerance.
3. The NL1 primary verdict is or is not logically sufficient for simultaneous native L and CL3-derived T success,
   judged from the actual source expressions and committed CL3 outcomes, without rerunning the expensive harness.
4. The equation-page single `eta(L)` core rule is or is not the same finite formula used in CL2/CL3's S9 cores,
   checked algebraically at the three tabulated masses and at the three committed crossover thresholds.
5. NL1's canonical-only linear approximation to T can be compared with CL3's three committed roots, separately on
   each footing. This is an audit of cached outputs, not an independent CLASS/EPS root solve.
6. Uncertainty omitted by treating ng48 reference medians as exact is illustrated by a fixed 2000-resample bootstrap
   of their nine recorded seeds (PCG64 seed 20261028). This is finite statistical evidence, not convergence proof.

## Outcome interpretation

- Recomputed cached medians / benchmark agreement authenticates these finite steps only.
- A primary-fixed-T pass does not establish a derived-T pass if the latter is not required by the verdict logic.
- Formula inequality is an implementation/documentation mismatch. It does not by itself regrade the observational
  line set or select a replacement physical rule.
- No ng64 result is graded before seven `ok` final snapshots; this audit never measures unfinished checkpoints.
- A live launcher/follower observation is time stamped and carries no completion ETA.

## Inputs and assumptions

| Input | Classification | Scope / provenance |
|---|---|---|
| X48 A2 per-seed JSON, S9 medians and measure() | FRAMEWORK-NATIVE numerical outputs / estimator | Finite ng48 collisionless zooms; not continuum convergence. |
| X43 cached collapse-column table; CL3 cached roots | FRAMEWORK-NATIVE under declared EPS and CLASS assumptions | Cached outputs only; CLASS Python binding is absent in current python3. |
| canonical / alt a0 and kappa=1/2 | fitted framework footing | Both footings remain separate. |
| LEE1 and CL2/CL3 grade records | inherited empirical calibration harness | Grades are read, not recomputed against raw observations in this bounded audit. |
| Live final-snapshot flags, run-log tails, process table | RAW operational observation | Snapshot of liveness only; no astrophysical inference from progress. |

No new parameter, fitting, parameter scan, data download, astrophysical simulation or empirical regrade is authorized.

## Determinism and controls

New script: `audit_native_l_t.py --output RUN_DIR`, with optional `--mutate` corrupting the median-reference check.
Run single-threaded, nice 15, maximum 60 s, maximum 1 GB address space. JSON output excludes clocks and runtime
statistics. A separate runner manifest records those. Two normal result JSONs must be byte-identical; the mutant
must fail its targeted check. Existing mutable simulation outputs are not inputs to the arithmetic run.

All numerical conclusions are conditional on IEEE floating arithmetic and the recorded JSONs. Full line-set grading,
an exact fresh EPS root solve, independent validation of the force/IC code, a covariant theory and continuum
convergence are explicit non-claims.

## Amendment A1 (pre-result; interpreter discovery)

The existing Miniconda Python interpreter supplies NumPy, SciPy and classy in isolated mode. Use that interpreter
for this audit. Add one independently coded background-A CLASS/EPS scalar calculation, following the documented
formulas and discretization of CL3: k=3000 logarithmic samples from 1e-4 to 150 h/Mpc, sigma squared on 191 mass
samples from logM=7 to 16.5, growth on 3001 redshift samples from 0 to 30, delta_c=1.686, half-mass coefficient
0.974 and virial density 18*pi^2. Read the background-A parameter vector from the existing F3 JSON. Use no galaxy,
cluster, lensing or zoom simulation data in this solver.

Compute constant-eta(L) and S9-eta(c_f(M)) roots on each footing at L=3.75, 3.9, 4.0 and the uncorrected 7.31
reference (a fixed diagnostic, not a scan to choose a passing value). The three existing CL3 constant-L roots must
reproduce within 0.002 dex; otherwise mark the scalar reproduction unsuccessful and keep any mismatch conditional.
Report the whole fixed table. This is a new bounded independent arithmetic experiment, not execution of the full
documented CL3 observational harness. It does not validate the EPS approximation or physical model.

## Amendment A2 (after launch failure, before any scientific result)

`run_001` failed before executing its child. A minimal diagnostic showed that macOS rejects setting RLIMIT_AS to
1 GiB (`ValueError: current limit exceeds maximum limit`), while RLIMIT_CPU=50 s succeeds. Retain the failed
manifest. Subsequent runs omit the unsupported address-space limit, keep the 60 s wall and 50 s CPU limits and
single-thread variables, and explicitly check observed peak RSS <1 GB. There is no enforceable address-space cap
for these runs; the resource claim is measured peak RSS only. No scientific criterion changes.
