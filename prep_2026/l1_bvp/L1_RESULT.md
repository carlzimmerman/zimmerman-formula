# l=1 Vector-Elastic BVP: w_l1(beta, kappa_t) — the banked directional-EFE debt, paid

**Date:** 2026-07-16
**Script:** `/Users/carlzimmerman/new_physics/prep_2026/l1_bvp/l1_bvp.py` (exit 0, all 14 gates PASS; full run log `l1_bvp.out`)
**Committed l=2 machinery reused (READ-ONLY, repo frozen):**
`zimmerman-formula/real_research/reviews/branchB_q2_gate_2026/vector_elastic_w_2026/methodA_ode.py`
(state system lines 82–88, moduli lines 11–12/49, forcing lines 14–15/79–80, BCs line 89),
`reduce_and_locate.py:27-29` (w reduction), `lane1_kappat.py` (kappa_t = 0.5 pin), `lane2_beta.py` (beta in (0,2), natural 2/7).

---

## 1. The debt

The directional-EFE prediction (`real_research/reviews/directional_efe_2026/laneA_predictions.py:390-399`,
caveat V1 of `confrontation.py`) used **A_BranchB ≤ w × A_AQUAL with w = w_l2 = 1/(1+4β/κ_t) = 7/23 = 0.304**
(natural β = 2/7, κ_t = 0.5) — an l=2 (Cassini quadrupole) number applied at l=1 (aligned dipole) as an
inequality, banked honestly as unproven. This solve pays it.

## 2. Setup: the l=1 BVP and how it differs from the committed l=2

**Identical to the committed solver except n = l(l+1):** the Takeuchi–Saito static spheroidal state
system y = [U, Σ_rr, V, Σ_rθ] with the exact RHS matrix of `methodA_ode.py:82-88`, **n = 2** (l=1)
in place of **n = 6** (l=2). Moduli: K_t(r) = K0hat·K_eff·max(1, r/r_t) (sqrt-branch tangent,
K_t = V''(J0) = K_eff/(2√J0), J0 = 2g_bar/a0V), μ_s = 3β·K_eff, λ = K_t − 2μ_s/3. Forcing: pure
gradient f = ∇(K_t·[J_target]_l), J_target = 2|g|/a0V, projected on P₁ instead of P₂ ((2l+1)/2
Legendre projection). BCs: traction-free inner, clamped outer (`methodA_ode.py:89`). Sun + uniform
g_ext background, both a0 footings, g_ext ∈ {1.9, 2.2, 2.6, 0.2} a0, K0hat ∈ {0.5, 1.0}.

**The l=1 zero-mode / gauge subtlety.** At l=1 the homogeneous exponents are {l−1, l+1, −l, −l−2} =
{0, 2, −1, −3}; the r⁰ solution is the **uniform translation** U = V = const, Σ_rr = Σ_rθ = 0 — zero
strain, zero stress, a gauge mode, not a deformation (verified: the RHS matrix annihilates [1,0,1,0]
to 9e-16). The physical l=1 response is the momentum-conserving relative-displacement sector,
isolated two ways: (i) the **observable is the dilatation J = U' + 2U/r − nV/r**, which on the
translation gives (2−n)c/r = 0 at n = 2 — translation-gauge-invariant *exactly, algebraically*;
(ii) the clamped outer boundary (medium anchored to the cosmological frame) removes the mode's
amplitude and absorbs the net force the l=1 forcing carries (via the Kelvin-like r⁻¹ branch) —
gated by rout-independence: w_l1 drifts ≤ 0.04% for rout ∈ [1e5, 1e6] AU.

**w definition (same as committed):** w = median(J_BVP/J_target) over the r_t shell (ρ ∈ [0.3, 1],
where K_t = K0hat·K_eff = the pinned κ_t) — the evaluation point at which the committed l=2 gives
0.304. One global forcing-sign factor calibrated against the committed μ_s→0 pure-bulk reference
(J = J_target exactly; `methodA_ode.py:14-15` — the committed P2 gate itself accepts the ratio by
magnitude, line 167); gated sign-uniform across l, β, radius.

## 3. Mandatory gates (all PASS, see l1_bvp.out)

| gate | result |
|---|---|
| l=2 indicial exponents {−4,−2,1,3} (committed target) | PASS |
| l=1 indicial exponents {−3,−1,0,2} incl. translation zero mode | PASS |
| μ_s→0 pure-bulk reference \|J/Jt\| = 1 | PASS (0.9921) |
| l=2 local P-wave law, committed shell 0.3<ρ<3 | PASS (ratio 1.0000 at β=0.1/0.33/0.95) |
| **l=2 re-solve reproduces committed w(2/7) = 0.304** | **PASS: 0.3043 vs 7/23 = 0.3043, dev 0.00%** |
| l=2 w(β) shape = 1/(1+8β) at 0.33/0.60/0.95/2.0 | PASS (dev 0.00% each) |
| convergence: gridN ×2/÷2, rout ×3.3/÷3, rin ×2/÷2.5, tol 1e-8 | PASS (max drift 0.044%) |
| guess-independence (pure-bulk and zero initial guesses) | PASS (identical to 5 decimals) |
| β→0 ⇒ w→1 (w(0.003) = 0.977) ; β large ⇒ w→0 (w(10) = 0.012) | PASS |
| sign uniform across l, β, radius | PASS |

## 4. Result: w_l1(β) at the r_t evaluation point (κ_t = 0.5, canonical; identical on alt footing)

| β | w_l1 (BVP) | w_l2 (BVP) | 1/(1+4β/κ_t) | w_l1/w_l2 |
|---|---|---|---|---|
| 0.05 | 0.7143 | 0.7143 | 0.7143 | 1.0000 |
| 0.10 | 0.5556 | 0.5556 | 0.5556 | 1.0000 |
| 0.20 | 0.3846 | 0.3846 | 0.3846 | 1.0000 |
| **2/7 (natural)** | **0.3043** | **0.3043** | **0.3043** | **1.0000** |
| 1/3 | 0.2727 | 0.2727 | 0.2727 | 1.0000 |
| **0.40 (β_crit canon, kt=0.5)** | **0.2381** | 0.2381 | 0.2381 | 1.0000 |
| **0.60 (β_crit alt, kt=0.5)** | **0.1724** | 0.1724 | 0.1724 | 1.0000 |
| 0.95 | 0.1163 | 0.1163 | 0.1163 | 0.9999 |
| 1.00 | 0.1111 | 0.1111 | 0.1111 | 0.9999 |
| **2.00 (all-shear corner)** | **0.0588** | 0.0588 | 0.0588 | 0.9999 |

At K0hat = 1.0 (saturated floor): w_l1(2/7) = 0.4667 = 1/(1+4β) — same l-equality. Footing spread
(canon vs alt a0, g_ext 0.2–2.6 a0): none to 4 decimals (w is dimensionless; a0 cancels).

**w_l1(β, κ_t) = w_l2(β, κ_t) = 1/(1 + 4β/κ_t) exactly (to 0.01%, BVP-proven).** The P-wave
admittance is l-independent: the gradient forcing drives only the longitudinal channel, and the
l=1 zero mode carries no strain, so it cannot enter the observable.

## 5. Verdict on the banked inequality — VALID at fixed κ_t, **INVALID as applied**

* **(a) l-structure: the banked structural claim was right.** At the same (β, κ_t) the l=1 transfer
  factor equals the l=2 one; A_B = w·A_AQUAL with the same w, no O(1) geometric coefficient.
  The "≤" was in fact "=" at fixed κ_t.
* **(b) Evaluation point: the bound was nonetheless INVALID as an upper bound on the aligned
  statistic.** The committed moduli themselves (`methodA_ode.py:11`) make κ_t run with radius:
  K_t = K_eff/(2√J0) stiffens as J0 = 2x/Z drops below 1. Cassini Q2 sources at ρ ~ 1 (J0 ~ 1,
  κ_t = 0.5, w = 0.304 — **the committed Cassini gate verdict is untouched**). The aligned RC
  statistic sources at the outermost RC points, x = g_bar/a0 ∈ [0.05, 0.5] (laneA X_GRID), i.e.
  ρ = √(y_c/x) ≈ 2.4–7.6, where local κ_t(x) = 0.5·√(y_c/x) = 1.2–3.8 and the **BVP-computed**
  suppression is much weaker:

  | β \ x | 0.50 | 0.30 | 0.20 | 0.10 | 0.05 | (r_t shell) |
  |---|---|---|---|---|---|---|
  | 2/7 | 0.513 | 0.576 | 0.625 | 0.702 | 0.769 | 0.304 |
  | 0.40 | 0.429 | 0.493 | 0.543 | 0.627 | 0.704 | 0.238 |
  | 0.60 | 0.334 | 0.393 | 0.442 | 0.529 | 0.613 | 0.172 |
  | 2.00 | 0.131 | 0.163 | 0.192 | 0.252 | 0.322 | 0.059 |

  BVP tracks the local law w = 1/(1 + (4β/K0hat)√(x/y_c)) to ≤0.02% at every point.

## 6. Corrected Branch-B prediction + rescaled N-targets (natural β = 2/7, K0hat = 0.5, canonical)

* **Aligned band:** A_B(x) = w_l1(x)·A_AQUAL(x) → **~0.5%–3.1%** (was banked <~0.3–1.2%).
  Branch B moves **toward AQUAL**: easier to detect against the null, harder to separate from AQUAL.
  Sign and shape (attractor-side-faster, EFE-reversal) unchanged.
* **3σ N-targets** (N = N_null/(1−w)², scaling reproduced against the committed
  `confrontation.out` table: 560/(1−0.3043)² = 1157 ✓). Representative outer point x = 0.107
  (confrontation's canonical footing) → w* = 0.695:

  | footing/env | banked (w=0.304) | corrected (w*=0.695) | x-band [x=0.5 … 0.05] |
  |---|---|---|---|
  | canon/maxclu | 1,157 | **~6,000** | 2,400 … 10,500 |
  | canon/noclu | 73,130 | ~380,000 | 149,000 … 663,000 |
  | alt/maxclu | 1,424 | ~7,400 | 2,900 … 12,900 |
  | alt/noclu | 90,085 | ~468,000 | 184,000 … 817,000 |

  **The canonical N ~ 1,157 rescales ×5.2 to N ~ 6,000** (max-clustering e_N). Detection-vs-null
  N (560 canon/maxclu) is unchanged — it does not involve w. The ×4.4–5.7 loop-orbit bracket-top
  and robust-σ reductions of confrontation.out still apply multiplicatively (bracket-top: ~310).
  WALLABY-scale (O(10³–10⁴)) still covers the AQUAL-vs-B separation only at the favorable corners.

## 7. Caveats (straight)

1. **Testbed geometry:** w_l1(x) is validated in the committed Sun+g_ext BVP geometry; the galaxy
   application goes through the local law with κ_t from the measured x = g_bar/a0. The BVP validates
   that local law to ≤0.02% at the relevant ρ, and it is guess-independent — but a full
   galaxy-geometry (disk + weak g_ext) l=1 solve remains the gold standard.
2. **κ_t(x) inherits lane-1's sqrt-branch tangent** (K0hat = 0.5 pinned). The saturated floor
   K0hat = 1.0 pushes w_l1(x) higher still — same direction, strengthens the correction. There is
   no defensible moduli reading that restores w = 0.304 at the RC radii.
3. **β stays lane-2 free in (0, 2)** (natural window 0.18–0.33). Even at the all-shear corner β = 2
   the aligned suppression at x = 0.1 is only w = 0.25, not 0.059: the "pure MI predicts exactly
   zero vs Branch-B <1%" contrast is *stronger* than banked (Branch B is now 0.5–3%), but the
   AQUAL-vs-Branch-B separation is *weaker*.
4. **Cassini unaffected:** Q2 sources at ρ ~ 1, where w = 0.304 at natural β stands; the committed
   Q2 gate verdict (w·Q2_scalar vs 5.2e-27 ceiling, β_crit ≈ 0.40/0.60) is not modified by this solve.

**Ledger action:** publish the correction — the banked A_B ≤ 0.304·A_AQUAL upper bound is retracted
for the aligned statistic and replaced by A_B(x) = A_AQUAL(x)/(1 + (8β)√(2x/Z)) (BVP-proven at l=1,
exact l-equality), with the N-targets above.
