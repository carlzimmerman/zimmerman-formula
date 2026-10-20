# Review and verification boundaries

2026-10-20. **Four partial Lean modules are kernel checked. The original
physical derivation of xi=1/4 is not established.** The separately supplied
real-pi adapter has not passed the current process memory cap.

## Analytic review

A fresh `fork_turns=none` reviewer `vector_completion_audit` independently
reconstructed MICROSCOPIC_CONTINUATION B-D from the raw action and proof.
It checked the full canonical constraint, open positive-root domain,
Dirac brackets, nonlinear energy, quadratic reduction, characteristic
polynomial, refined cones, finite-ball variational/comparison argument,
global barriers, radial asymptotic and uniqueness. It never saw checker
outputs or compiled Lean. It found no remaining issue within that
specified classical scope.

Review caused explicit precision fixes: exclude the constant-phi zero
mode for strict quadratic positivity, subtract epsilon0 when discussing
logarithmic total-energy divergence, restrict uniqueness to radial y
(phi retains a constant), and remove the claim that kV=1 means uncoupled.
The result remains a preferred-clock classical theory on Y>0, A=0
backgrounds, not arbitrary phase-space, quantum, clock or gravity health.

The same reviewer independently differentiated section A's common-scale
potential and checked its total amplitude dictionary. It found an actual
overstatement: a strict local minimum need not have positive-definite
Hessian. The corrected statement requires strict quadratic stability for
the strict Schur inequality; an ordinary minimum gives a weak inequality.
The counterexample epsilon+(chi-1)^4+(d-1)^2 is preserved in this audit
record. The single-log positive-energy exclusion survives because its
radial curvature is strictly negative. The current raw proof was reread
and passed with these qualifications at SHA256

    dda2a375727cdd76ba60801d763302af1e34d13af962e070d9a77a30055dde19.

The charged pressure/BMB continuation was derived by the independent
read-only `gap_selection_physics` route, which reported a separate fresh
check of its spectra and conditional charged minimization. The coordinator
also recomputed the key stationary/pressure and Gauss equations. This is
route-level analytic checking, not a separate fresh audit of the final
REGULAR_PRESSURE_PARENT text or a full real-time quantum proof.

## Formal verification

The exact final records selected by check_evidence.py are:

| Source | Evidence directory | Exit |
|---|---|---|
| PairedBandStress.lean | runs/final_stress_exported | 0 |
| AmplitudeBridge.lean | runs/final_amplitude_types | 0 |
| ScaleGap.lean | runs/final_scale_audited | 0 |
| GaugeCones.lean | runs/final_cones | 0 |
| controls/Normal.lean | runs/final_controls_normal | 0 |
| controls/ReversedStress.lean | runs/final_controls_reverse | 1, expected False |
| controls/VacuumOffset.lean | runs/final_controls_vacuum | 1, expected False |

The four modules print 25 critical theorem types and axiom lists. Every
list is exactly propext, Classical.choice, Quot.sound. The separate normal
control compiles, while both mutants reduce to an unsolved False goal;
neither failure is an import or fixture error. Their rational contexts
are consistent and explicit. They do not test or certify a quantum model.

PairedBandStress and GaugeCones were implemented in isolated write scopes
by `formal_target_obstruction`, then independently recompiled by the
coordinator. AmplitudeBridge and ScaleGap were implemented and checked by
the coordinator. Their proof terms are kernel checked; there is no claim
that a distinct human or fresh agent audited every Lean source line.
Physical-to-formal dictionaries remain exposed in the module statements
and README. Agreement is not a formal certificate for the physical leaves.

## Preserved implementation failures

Legacy Lean import mode loaded private transitive code and exhausted the
memory budget. An imports-only probe and the installed Lean source
identified the cause; explicit module/public/meta imports fixed it under
the same 1024 MiB limit. Ring.Basic exports ring1; legacy private imports
had concealed this interface issue. New-module exported definitions also
needed expose for client controls to unfold them. A normalization proof
needed an explicit arithmetic rewrite on an iff goal. All failed logs
and source snapshots remain diagnostic history, not accepted evidence.
Some failed elaborations print sorryAx; none of the successful final
modules does, and no source proof admission was added.

Initial agent attempts used a higher limit before the coordinator imposed
the campaign light-job cap; those commands are disclosed in dev_stress.
All final runs use one worker, 1024 MiB, 30s CPU and 45s wall. A current
resource inspection confirmed a large simulation remains live. PiBridge's
analysis import still exhausts this cap and is deferred; the cap was not
raised. Earlier manifests whose input hashes predate corrections are
historical. VERIFIED.json selects only current successful modules and
the two genuine expected-failure controls.

The installed toolchain is Lean 4.34.0-rc2, Lean commit
6a10ac8c22beadecabdbb0919c2b50214762f91d; mathlib is pinned at
85e3a25e006c35636f0e53b0e9296caca2685bc0. Exact source/dependency/log hashes
are in the manifests. Local imported objects require matching source and
object stamps. Reproduction requires the pinned existing library and
compiling the four sources in the order shown in README.

Conservative mathematical self-proofreading covered the new proof/report
files and their final corrections. Substantive corrections above belong
to proof audit. There were no further mathematical-token changes from
proofreading and no additional document build was required.

Evidence checkpoint f77a0cd8d preserves the raw diagnostic logs. The
compiler warning in dev_stress/attempt02.log has one trailing space;
git diff --check flags that raw output, which is intentionally unchanged
so its recorded hash remains accurate. Source and report files have no
reported whitespace defects. The campaign regeneration after K673-K678
passes all four checks and adds no determinate normalization trial.

The neutral-current follow-up received a separate independent analytic
audit at SHA256
5f22ea960ef195963e1a3bf3ab7212c6792082efb99f831ac81426cdaccf7551.
Verdict: proved as written under its explicit ensemble and affine-gradient
hypotheses. The audit checked the neutral solution, pressure/charge/stress,
fixed-charge Hamiltonian/Hessian, exact dilute current, concavity and
joint-pressure Hessian. It did not certify a general microscopic no-go,
quantum theory or Lean proof. No correction was required.
