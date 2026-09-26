# R01 — Certify the actual active-density asymptote (result)

- Owner: Hermes (this lane); independent reviewer: none yet (self-review recorded)
- Execution state / claim state: completed / proved_conditional (numerics) + proved (algebra)
- Baseline commit and actual inputs: base `3e857b5a6f8f05b48e29d0cbe42136998e9f9445`
  (followup work order); source inputs read from HEAD at run time:
  `real_research/clock_2026/L304_phantom_active_mass.py` (unmodified),
  `real_research/clock_2026/L298_phantom_stress_tensor.py` (unmodified); repo HEAD
  `29b5c74ff`.  `python3 exact_factorization.py` exit 0.
  `ActiveDensity.lean` compiled with `lake env lean` exit 0, zero `sorry`,
  axioms = [propext, Classical.choice, Quot.sound].
- Model/action ID: L304 surrogate (the L298 stress's Poisson face), unchanged.

## Exact claim and scope

For B,D>0, 0<K<2, u>0: (w-1)rho = (2/3)(2-K) D u^3 exactly (not asymptotic).
With u(B+u)=A/r, A>0: r*u -> A/B and r^3 rho_act -> (2/3)(2-K) D (A/B)^3.
Scope: the L304 surrogate only; NOT the complete covariant stress, NOT a claim
about other kernels.

## First discriminator and result

**7/7 PASS.**  The factorization (N1) is exact for every u>0 — the
B + (2/3)u factor cancels.  N2-N3 prove r*u -> A/B and the C/r^3 asymptote
symbolically and numerically.  N4: on L304's own 1-100 Mpc window the profile
already sits on the shell (r^3 rho_act within 0.05% of its asymptote at the
window end).  **N5: the 0.58 slope L304 quotes is reproduced by a pure
C/r^3 shell integrated with zero interior mass on the same window (fit 0.578),**
so the "sqrt(r)" reading of L304 V4 is a finite-window artifact of the log
shell — M_act = M0 + 4πC ln(r/r0), not K sqrt(r).  N6: with M0 (2.5e42 kg
below 1 Mpc) tracked, the active mass is linear in ln r to 0.06%.  N7: the
finite-radius remainder bound |r^3 rho_act − C| ≤ 3CA/(B²r) holds.

## Evidence

- `exact_factorization.py` → exit 0, 7/7 checks PASS (N1–N7), results JSON.
- `ActiveDensity.lean` → exit 0; `#print axioms` = standard three only.
  Formalized: factorization, (w−1) ∈ (0,1), the r³ asymptote rearrangement,
  the rationalized-root identity.  NOT formalized in Lean: the limit statements
  themselves (numeric N2/N4/N7 carry them); formalization status recorded.

## Independent check

N5's control: the pure log shell integrated from the cutoff gives 0.578 on the
identical window and sampling; L304's own V4 gate (0.4–0.7) would "pass" a
logarithm.  This is the adversarial control that isolates the artifact.

## Novelty and physical interpretation

Correction to L304 V4's reading ("M_act ~ r^0.58 = sqrt(r)") and L311 V2's
r^{1/8} rise: the surrogate's asymptote is logarithmic.  The RAR-stability
conclusion (the phantom's self-gravity cannot re-feed the EFE) SURVIVES — a
log grows slower than sqrt — but the specific shape prediction attached to
sqrt(r) does not.  Nearest sources: L304, L311 (this repo); their claims are
modified, not confirmed.

## Decision and next action

proved_conditional (limits: numeric) / proved (algebra).  Pass the shell
constant C and the M0 value + remainder bound to R02 (done) and R03 (done);
the square-root continuation should no longer be used in L311's outer-rise
prediction.  Dependent: R02, R03, F2, E1.  Next cheap test: R19's log-mass
control against L311's pipeline (the fitted-power gate).