# ADVERSARIAL VERIFICATION — l=1 vector-elastic BVP (w_l1) solve

**Date:** 2026-07-16
**Verifier artifacts:** `verify_l1_independent.py` (exit 0, 12/12 independent checks PASS; log `verify_l1_independent.out`)
**Under test:** `l1_bvp.py` + `L1_RESULT.md` (this directory)

## VERDICT: **UPHELD** (all four verification lanes pass; one framing note, no corrections)

---

## 1. Re-run of the solve under test

`l1_bvp.py` re-run 2026-07-16: **exit 0, 14/14 gates PASS**, output byte-consistent with `l1_bvp.out`
(w_l1(2/7) = 0.3043, w(x) profile 0.513–0.769, corrected N-targets 6,007 / 379,641 / 7,391 / 467,659).

Claimed verbatim reuse of the committed l=2 formalism **verified against the frozen source**:
`branchB_q2_gate_2026/vector_elastic_w_2026/methodA_ode.py` — RHS matrix (lines 82–88) identical with
only n = l(l+1) generalized; moduli `kt = K0hat*max(1,rho)` (line 49) identical; forcing
`phi = kt*Jt_l`, `Fr = dphi/dr`, `Fth = phi/r` (lines 79–80) identical; BCs `[Ya[1],Ya[3],Yb[0],Yb[2]]`
(line 89) identical; local-law guess (line 90) identical. The Legendre projection generalizes
methodA's hard-coded 2.5·⟨Jt·P2⟩ (lines 41–48) to (2l+1)/2·⟨Jt·P_l⟩ correctly. **No re-derivation drift.**

## 2. Independent l=1 solve by a different method (V1)

Global **box scheme** (trapezoidal, 2nd order) assembled as one sparse linear system, **direct sparse-LU
solve — no initial guess exists** (the problem is linear), vs the solve-under-test's guess-seeded
adaptive-collocation `solve_bvp`. Second independent extraction: **harmonic-projected least squares**
J = w·Jt + a·ρ^l + b·ρ^−(l+1) over the constant-moduli shell — the two power laws are *exactly* the
homogeneous dilatation modes there (div of Navier: (K+4μ/3)∇²J = ∇²Φ ⇒ J − w·Jt harmonic), so this
extraction projects out homogeneous/zero-mode-adjacent contamination analytically rather than relying
on the median.

* l=1, all 10 betas of the claim table: **w_median and w_fit agree with l1_bvp.py and with
  1/(1+8β) to <0.01%** (e.g. β=2/7: 0.30434/0.30435 vs claimed 0.3043).
* Harmonic contamination in the shell: ~2e-5 of the signal — the shell median was never at risk.
* Analytic structure: the l-independence of w is not just numerics — the particular solution of
  (K+4μ/3)∇²J = ∇²Φ is J = Φ/(K+4μ/3) = w·J_target at **any** l for constant moduli; l enters only
  through the homogeneous terms, which the BCs make negligible in the shell. The BVP result is the
  expected analytic answer.
* w(x) profile at the RC radii (V3): box scheme gives 0.5128/0.5761/0.6247/0.7018/0.7689 at
  x = 0.5/0.3/0.2/0.1/0.05 — matches l1_bvp.py (0.513–0.769) and the local law
  w = kt/(kt+4β), kt = 0.5√(y_c/x), to <0.1%.

## 3. l=2 reproduction against the frozen repo (V1b + frozen re-runs)

* Frozen `lane2_beta.py` re-run (read-only): prints **"canonical kappa_t=0.5: w=0.304"** at natural β —
  the committed anchor confirmed from the frozen repo itself, exit 0.
* Frozen `methodA_ode.py` re-run (read-only, exit 0): published w rows reproduced
  (canon g=2.2, K0hat=0.5: w = 0.286/0.181/0.122/0.062 at β = 0.33/0.60/0.95/2.0). Note these
  projected-Q2 w's sit slightly **above** the pure formula (0.275/0.172/…) precisely because the
  committed pipeline itself applies the suppression **radius-dependently** (Ssup(r), methodA_ode.py:153)
  — the committed machinery already treats κ_t as running with radius, which **corroborates** the
  "invalid-as-applied" finding rather than undercutting it.
* My box-scheme at n=6: w_l2(2/7) = **0.30435 = 7/23 exactly** (dev 0.000%), and the full β-shape
  1/(1+8β) at 0.33/0.60/0.95/2.0 to 0.000%.
* Frozen `confrontation.out` N-table read directly: 560→1157, 35390→73129, 689→1424, 43595→90084 —
  the banked numbers l1_bvp.py anchored to are the real committed ones. The banked inequality caveat
  is verbatim at `directional_efe_2026/laneA_predictions.py:388-399` ("an explicit l=1 BVP … has NOT
  been run … the INEQUALITY A_B <= w_max x A_AQUAL is the robust statement") — the debt is as described.

## 4. Zero-mode attacks (V2 — the classic l=1 trap)

* **Z1 (gauge invariance):** added a rigid translation c·[1,0,1,0] with amplitude 10× the physical
  response to the solved state and recomputed the observable: **Δw/w = 7.3e-16** (machine zero).
  J = U′ + 2U/r − nV/r annihilates the translation algebraically at n=2, as claimed. The classic
  failure mode (rigid displacement absorbed into the response) **cannot** contaminate this observable.
* **Z2 (BC-independence of the mode removal):** re-solved with two *different* translation-killing
  outer BC pairs — (U=0, Σ_rθ=0) and (Σ_rr=0, V=0) — vs the committed clamped (U=V=0):
  w_l1 = 0.30435 / 0.30426 / 0.30434, **spread 0.031%**. The answer does not depend on *how* the
  zero mode is killed.
* **Z3 (momentum bookkeeping):** at l=1 the forcing carries a net z-force; computed the outer-anchor
  traction integral 2πr²(Σ_rr·2/3 + Σ_rθ·4/3) against the volume force integral:
  **imbalance 6.4e-6 relative** — the clamped anchor absorbs the net force exactly as the physical
  argument requires; nothing leaks into the sourcing shell (consistent with the 0.04% rout-drift gate).

## 5. N-target arithmetic (V4)

Exact recomputation from the frozen N_null values: banked row 560/(1−7/23)² = 1157 ✓ (=confrontation.out);
w*(x=0.107) independently = 0.6947; corrected N = **6,007 / 379,641 / 7,391 / 467,659** — 0.00–0.01%
agreement with l1_bvp.py's table; rescale factor (1−0.3043)²/(1−0.6947)² = **5.19 ≈ ×5.2** ✓; corrected
aligned band w(0.5)×1% … w(0.05)×4% = **[0.51%, 3.08%]** ✓. Detection-vs-null N (560) indeed does not
involve w and is unchanged. β=2 spot check: w(x=0.1) = 2.69/(2.69+8) = 0.252 ≈ 0.25 as stated.

## 6. Verdict detail

* **(1) w_l1(β,κ_t) = w_l2(β,κ_t) = 1/(1+4β/κ_t) at fixed κ_t** — CONFIRMED by an independent
  discretization, an independent extraction, and the analytic constant-moduli argument. The banked
  "≤" was indeed "=" at fixed κ_t; no O(1) l-geometric coefficient.
* **(2) Invalid-as-applied finding** — CONFIRMED. The committed moduli law K_t = K_eff/(2√J0)
  (methodA_ode.py:11, lane1's own sqrt-branch pin) makes κ_t = 0.5√(y_c/x) at the RC sourcing radii
  x = 0.05–0.5 (laneA X_GRID confirmed at laneA_predictions.py:275), where the BVP gives w = 0.513–0.769,
  not 0.304. Using 0.304 as an *upper bound* on the aligned statistic contradicts the committed moduli;
  the retraction+replacement A_B(x) = A_AQUAL(x)/(1+8β√(2x/Z)) is the correct ledger action. Note the
  correction *helps detectability vs the null* and *hurts AQUAL-separability* — reported straight, not
  a manufactured win in either direction.
* **(3) Cassini untouched** — CONFIRMED: Q2 sources at ρ~1 where the same solve still gives 0.304; the
  frozen methodA/lane2 verdicts (β_crit ≈ 0.40 canon / 0.60 alt) are unmodified.

## 7. Framing note (no correction required)

`L1_RESULT.md` calls w = median over ρ∈[0.3,1] "the identical evaluation point that gives the committed
l=2 0.304". Precisely: the committed 0.304 is the `reduce_and_locate.py:27-29` **formula** value at the
lane-1 pinned κ_t = 0.5 (the r_t-shell reading), which the shell median reproduces to 0.00%; methodA's
own *projected* Q2-weighted w at the same footing is a few % higher (0.286 vs 0.275 at β=0.33) because
its projection samples ρ>1. The banked laneA number is the formula value, so the anchoring is correct;
just don't read "identical evaluation point" as "methodA's Q2 projection integral".

Caveat 1 of L1_RESULT.md (Sun+g_ext testbed geometry, not a disk) stands as the honest residual: the
galaxy application rests on the local law, which the BVP validates in this geometry to ≤0.02%; a
disk-geometry l=1 solve remains the gold standard.
