# M01 — ALGEBRAIC SPINE: LEAN VERDICT

**2026-09-23 · lane: fable_independent_2026/lean_2026/M01_alg_spine.lean · exit 0 · zero sorry · axioms exactly {propext, Classical.choice, Quot.sound}**

Toolchain: Lean 4.34.0-rc2, `lake env lean M01_alg_spine.lean` from
`fable_independent_2026/lean_2026/` (mathlib rev v4.34.0-rc2, local cache),
compile seconds ≈ 5, exit code 0.  Axiom check: `#print axioms` for every
theorem at the end of the file — all 32 theorems print
`[propext, Classical.choice, Quot.sound]`, no `sorryAx`, no `sorry` anywhere.
Nothing in this lane touches I21/I22/I23/I24; no git commit.

Classification legend: **CERTIFIED** = Lean theorem, proof complete, axioms clean.
**CONJECTURED-WITH-NUMERIC-EVIDENCE** = formally stated in Lean (a `def` : Prop),
no proof given/possible in current mathlib with the allowed toolkit, backed by
machine numerics quoted verbatim.

---

## 1. Central window-ratio law: W(q) = (1+q/3)/(1/2+q/4), q ≥ 0  — ALL CERTIFIED

| theorem (namespace M01) | statement (Lean) | status |
|---|---|---|
| `windowRatio_eq` | `2 + q ≠ 0 → windowRatio q = (4/3)·(3+q)/(2+q)` | CERTIFIED |
| `windowRatio_zero` | `windowRatio 0 = 2` (endpoint 2) | CERTIFIED |
| `windowRatio_gt_four_thirds` | `0 ≤ q → 4/3 < windowRatio q` (strict: 4/3 only at q→∞) | CERTIFIED |
| `windowRatio_le_two` | `0 ≤ q → windowRatio q ≤ 2` | CERTIFIED |
| `windowRatio_antitone` | `0 ≤ q' → q' ≤ q → windowRatio q ≤ windowRatio q'` (decreasing in q) | CERTIFIED |
| `windowRatio_limit` | `∀ ε>0, ∃Q, ∀q ≥ Q, |windowRatio q − 4/3| < ε` (endpoint 4/3, explicit ε−Q, no calculus) | CERTIFIED |

J09 numeric anchor (deepseek_push/J09_two_component_law.out, 27/27 PASS):
exact_ratio 2.0 (q=0), 1.4444444444444446 (q=10, τ₀=1), 1.6 (q=3, τ₀=2) — all inside (4/3, 2].

## 2. Generalized-p window: S_p(q) = (1+q/(p+1))/(1/2+q/(p+2))  — ALL CERTIFIED

Certified for **real p ≥ 1**, hence in particular every integer p ≥ 1
(corollary `windowRatioP_int`).  Endpoint L_p = (p+2)/(p+1).

| theorem (namespace M01) | statement (Lean) | status |
|---|---|---|
| `limitP_one` | `limitP 1 = 3/2` | CERTIFIED |
| `limitP_two` | `limitP 2 = 4/3` (central special value) | CERTIFIED |
| `windowRatioP_zero` | `windowRatioP p 0 = 2` | CERTIFIED |
| `windowRatioP_eq` | `1 ≤ p → 0 ≤ q → windowRatioP p q = limitP p + p(p+2)/((p+1)(p+2+2q))` (exact distance to the limit) | CERTIFIED |
| `windowRatioP_gt_limit` | `1 ≤ p → 0 ≤ q → limitP p < windowRatioP p q` (strict lower end) | CERTIFIED |
| `windowRatioP_le_two` | `1 ≤ p → 0 ≤ q → windowRatioP p q ≤ 2` | CERTIFIED |
| `windowRatioP_antitone` | `1 ≤ p → 0 ≤ q' → q' ≤ q → windowRatioP p q ≤ windowRatioP p q'` | CERTIFIED |
| `windowRatioP_limit` | `1 ≤ p → ∀ε>0, ∃Q, ∀q ≥ Q, |windowRatioP p q − limitP p| < ε` with witness Q = (p+1)/(2ε) | CERTIFIED |
| `windowRatioP_eq_two` | `windowRatioP 2 q = windowRatio q` (family contains the central law) | CERTIFIED |
| `windowRatioP_int` | `1 ≤ n (natural) → 0 ≤ q → limitP (n:ℝ) < windowRatioP (n:ℝ) q ∧ windowRatioP (n:ℝ) q ≤ 2` (integer-p formulation) | CERTIFIED |

J09P numeric anchor (deepseek_push/J09p_general_p.out, 21/21 PASS): p=1 q=5 exact
1.6154 limit 1.5; p=2 q=5 exact 1.5238 limit 1.3333; p=4 q=20 exact 1.3043 limit
1.2 — measured ratios inside (L_p, 2] exactly as certified.

## 3. Slack boundary identity: slack = 1/ρ²  — CERTIFIED

| theorem (namespace M01) | statement (Lean) | status |
|---|---|---|
| `slack_boundary_identity` | `eD ≠ 0 → eA ≠ 0 → eDA ≠ 0 → (eD·eA)² / eDA² = 1 / ((eDA/(eD·eA))²)` — with ρ = E[D·ang]/(E[D]·E[ang]) this is exactly slack = 1/ρ² | CERTIFIED |

## 4. Two-component factorization and J10-I = (r_B/R)·window  — ALL CERTIFIED

| theorem (namespace M01) | statement (Lean) | status |
|---|---|---|
| `window_from_components` | `τ₀ ≠ 0 → 0 ≤ q → (τ₀(1+q/3)) / (τ₀(1/2+q/4)) = windowRatio q` (quotient of the −ln A and E[D] component identities) | CERTIFIED |
| `j10i_factorization` | `R ≠ 0 → d ≠ 0 → (a·r_B)/(R·d) = (r_B/R)·(a/d)` (J10-I factorization) | CERTIFIED |
| `j10i_window_decomp` | `0 ≤ q → 0 ≤ r_B → 0 < R → 4/3·(r_B/R) ≤ windowRatio q·r_B/R ∧ windowRatio q·r_B/R ≤ 2·(r_B/R)` | CERTIFIED |

## 5. K04 inversion bijection (s,d) = (−ln A, E[D]) ↔ (τ₀, q)  — ALL CERTIFIED

Definitions: `tau0Hat A d = −3·ln A − 4·d`, `qHat A d = 4·d/tau0Hat A d − 2`,
and the s-forms `tau0Of s d = 3s − 4d`, `qInvOf s d = 4d/tau0Of s d − 2`
(the linear-system inversion of τ₀(1+q/3) = s, τ₀(1/2+q/4) = d).

| theorem (namespace M01) | statement (Lean) | status |
|---|---|---|
| `k04_tau0Hat_eq`, `k04_qHat_eq` | A-form = s-form under s = −ln A | CERTIFIED |
| `k04_recover_s`, `k04_recover_d` | `tau0Of ≠ 0 → τ₀(1+q̂/3) = s` and `τ₀(1/2+q̂/4) = d` (inversion returns the data) | CERTIFIED |
| `k04_recover_A` | same in A-form: `τ̂₀(1+q̂/3) = −ln A` | CERTIFIED |
| `k04_roundtrip_tau`, `k04_roundtrip_q` | `τ₀(s(τ,q),d(τ,q)) = τ`, `q̂(s(τ,q),d(τ,q)) = q` | CERTIFIED |
| `k04_window_forward` | `0 < τ → 0 ≤ q → 4d/3 < s ∧ s ≤ 2d` (forward bijection into the window) | CERTIFIED |
| `k04_window_backward` | `4d/3 < s → s ≤ 2d → 0 < τ₀(s,d) ∧ 0 ≤ q̂(s,d)` (backward bijection) | CERTIFIED |
| `k04_qhat_gt_neg_one` | `0 < τ̂₀ → (q̂ > −1 ↔ 8·E[D] > −3·ln A)` — the CORRECTED boundary, checked against the data | CERTIFIED |
| `k04_qhat_nonneg` | `0 < τ̂₀ → (q̂ ≥ 0 ↔ s ≤ 2d)` (upper edge of the window) | CERTIFIED |
| `k04_refutes_ed_three_halves` | `∃ A d, 0<A ∧ A<1 ∧ 0<d ∧ d<3/2 ∧ qHat A d < −1` — witness A = e⁻¹, d = 1: **the suggested "q̂ > −1 ⟺ E[D] < 3/2" is FALSE**; e.g. E[D] = 1 < 3/2 yet q̂ = 4/(3−4) − 2 = −6 < −1. The task instruction "check the algebra yourself and certify what is true" is applied: the true boundary is 8·E[D] > −3·ln A (given τ̂₀ > 0), certified above. | CERTIFIED |

## 6. Chord moment ⟨chord⟩_vol = 3/4  — CONJECTURED-WITH-NUMERIC-EVIDENCE (honest)

Statement (formalized as `M01.chordMomentConjecture : Prop` — a `def`, so it
compiles with zero axioms and zero sorry, but it is **not** a proved theorem):

    chordVol r μ = rμ + √(1 − r²(1−μ²))
    chordMomentVol = 3 · ∫₀¹ r²·(½·∫₋₁¹ chordVol r μ dμ) dr
    chordMomentConjecture : chordMomentVol = 3/4

**Not certified in Lean.**  The natural proof is a 2D change of variables
(r,μ) ↦ (r√(1−μ²), rμ) (bijection [0,1]² → quarter unit disk, dr dμ =
√(1−μ²)/r du dv, reducing the integral to ∫∫_{quarter disk} u√(1−u²) du dv =
∫₀¹ u(1−u²) du = 1/4, hence 3·(1/4) = 3/4; the rμ term vanishes by μ-oddness).
mathlib's interval-integral toolkit has no 2D substitution theorem, so this
proof cannot currently be carried out in Lean without importing heavyweight
measure theory beyond the allowed scope.  Per the task rule, we SAY SO instead
of pretending: no fabricated certificate.

Numeric evidence (deepseek_push/J11_VOLUME_WINDOW_VERDICT.md, verbatim):
"Closed-form anchor: **⟨chord⟩_vol = 0.750000 exactly** (uniform interior
point, isotropic direction; quadrature ng=80 → 0.750000; cf. central = 1.0,
surface = 4/3 ≈ 1.3333)".  Additional quadrature agreement in
J11_volume_atom.out: q=0 volume atoms 0.70743/0.70728 (τ₀=0.5),
0.52793/0.52725 (τ₀=1), 0.33297/0.33242 (τ₀=2), 0.23674/0.23635 (τ₀=3),
z ≤ 0.86 for MC vs Gauss–Legendre — the same integrand quadrature pipeline
that produced 0.750000.

---

## Summary of counts

- Certificates: **32 Lean theorems CERTIFIED** (sections 1–5; includes the
  explicit refutation `k04_refutes_ed_three_halves`), all exit-0 on the single
  file, matching the `#print axioms` list exactly (32 names, no sorryAx).
- Conjectures: **1** (`chordMomentConjecture`) — CONJECTURED-WITH-NUMERIC-EVIDENCE.
- `sorry` count: 0.  Axioms (verified `#print axioms` per theorem): exactly
  {propext, Classical.choice, Quot.sound}.
- Files: `fable_independent_2026/lean_2026/M01_alg_spine.lean` (written),
  `deepseek_push/M01_ALG_SPINE_VERDICT.md` (this file),
  `deepseek_push/M01_results.json`.  No git commit; I21–I24 untouched;
  scratch probes `_probe_m01*.lean` removed.