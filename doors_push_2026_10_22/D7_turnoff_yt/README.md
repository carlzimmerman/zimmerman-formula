# D7_turnoff_yt — origin of the strong-field turn-off (P5) and its scale y_t

## Verdict: SCOPED NO-GO

The canonical law needs a turn-off. Nothing in the action supplies one. P5 stays a posit on the law.
Its scale y_t is κ under another name, and no data on disk can measure it.

Script: `d7_turnoff_yt.py` gives 11/11 PASS in under 1 s. The `--mutate` run (RAR kernel, tail 0) gives 3/11.
Criteria were frozen first in `FROZEN_CRITERIA.md` (commit f2e0423a60). Every number below is in
`d7_turnoff_yt_results.json`.

## The numbers

**Q1. Does the canonical law itself need P5? Yes.**
- From `g_N = g²/(g+a₀)` we get `ν − 1 = (√(1+4/y) − 1)/2`. Its tail is `y(ν−1) → 1`, so the anomaly is a
  constant **a₀**. The quadrature law's tail is a₀/2 (K1, sympy).
- At 1.5 AU the bare anomaly is **2557.4 × B_E** on the canonical footing and **3087.4 ×** on the alt footing.
  The quadrature law gives 1278.7 and 1543.7 × (K2). So P5, or some other turn-off, is needed on both footings.
  This confirms A4. The DSF-21 BRIEF's "open for lane C2" is stale.
- The external field does not help (K3). We added the Galaxy's Newtonian field (from A60) to the
  algebraic QUMOND phantom source at 1.5 AU. The local phantom density changes by at most 2.7e-8 (canonical)
  and 3.3e-8 (alt). The angle-averaged monopole, which sets the radial anomaly by Gauss's law, is unchanged
  to 1e-9. The tidal term is about a₀·r/r_M = 1.9e-4 a₀. An O(10²) EFE suppression cannot apply to a 1/y tail.
- With P5 at the closure y_t, the 1.5 AU anomaly falls to 1.4e-8, 1.2e-8 and 2.0e-8 × B_E
  (κ = ½, alt and thermal points; K4).

**Q2. Is the closure a constraint or an identity?**
- `F(y_t)` is strictly increasing (K6), so `I(y_t) = 8π/κ²` is a one-to-one relabelling of κ, not a
  logical tautology. Every κ gets exactly one y_t: 66.2999 (quoted Λ, a₀), 66.3803 (32π), 46.0148 (alt),
  and **77.876** at the thermal postulate, where 8π/κ² = 118.435 (K5).
- The falsifier band y_t ∈ [60, 140] is exactly κ ∈ [0.3415, 0.5267] (K6). It is a κ statement.
- y_t has no independent observable today (K7):
  - The planetary signal scales as `a₀(y_t/y)²`. Even at y_t = 140 the best planet (Saturn) sits at
    **5.5e-4 of its published bound**.
  - In wide binaries, moving y_t from 60 to 140 changes g by at most **0.57 %**, at y ≈ 50
    (s ≈ 1600 AU for 2 M⊙).
  - So "y_t tied to Λ" has no testable content now beyond the κ it encodes.

**Q3. Is there a mechanism in the action? No. Three obstructions are named.**
- **Stiffness L★ (K8, K9).** The γ term does suppress the law, but the trigger is mass, not acceleration.
  - In the saturated regime, gradient ÷ saturation = **M_crit/M**, with no y in it. The script measured
    1.0009e-3 for M = 10³ M_crit.
  - At y = 66 the anomaly is 0.985 a₀ for M = 10³ M_crit and 1.0e-3 a₀ for M = 10⁻³ M_crit.
  - The Sun is 1.5e-7 to 2.6e-6 of M_crit over both footings and L★ ∈ [24, 90] pc. So a stiffness cure of the
    planets (residual a_P ≤ 6.6e-3 B_E) is the medium-first reading. A26 rejects that reading at 21σ on the
    45 sub-M_crit dwarfs (external input).
- **Gate saturation W(u) (K10).** In spherical symmetry the anomaly equals u exactly (A22). P5 makes the
  anomaly non-monotone in g. At y_t = 66.30 it peaks at y = 12.24 with u = 0.899 a₀. The same u then occurs
  at g = 0.816 a₀ and at g = 72.9 a₀, so `g = K W'(u)` would need two values.
  - **No gate potential W(u) can produce P5**, at any y_t in [60, 140] or at the alt point.
  - Saturation is what *creates* the a₀ tail; it cannot also remove it.
  - A turn-off needs a new invariant, for example a nonlinear clock coupling f(|∇ln N|), and that brings its
    own constant.
- **Scale candidates (K11).** We froze 48 monomials `(cH_Λ/a₀)^m (c²/(a₀L★))^n`, with m, n ∈ {0, ±½, ±1, ±2}.
  None lands within 5 % of y_t at all three points (κ = ½, alt, thermal). The closest misses by 50 %.
  - A coincidence was disclosed before freezing: `(c²/(a₀L★))^{1/5} = (c/σ_c)^{2/5} = 66.46`. It is +0.2 %
    at κ = ½ but **+44 % alt** and −15 % thermal, because it does not depend on the footing while y_t does.
    It is numerology.
  - A28's `2Z²` near-miss remains what A28 called it: the coefficient 2 is inserted.

## Errors found in the record

- `deepseek_push/DS_FINAL_2026_10_21/BRIEF.md:41-47` says whether the canonical law needs the cure is
  "open". A4 already answered it (2557×), and K2 here confirms it.
- `THEORY.md:155` and `CANDIDATE_LAWS_REGISTER.md:677` say "planets pass 9.14×". That margin comes from a
  **stand-in** Neptune bound, which A4 flags as `published_bound: false`. With published bounds only, the
  margin is 90× in y_t, and the signal is 1.2e-4 of Saturn's bound at y_t = 66.3.
- `A4_ppn/report.md:220-222` says "the repo's earlier EFE estimate is an O(10²) suppression". That cannot
  apply to a 1/y tail: K3 finds the monopole unchanged to 1e-9.
- Thermal y_t is inconsistent inside THEORY.md: 77.85 at lines 308, 354 and 457, but 77.944 at line 445, and
  Λc⁴/a₀² = 118.6 at line 457. 8π/κ_th² = 118.435 gives **77.876**; 118.6 would give 77.98.

## What this does not show

- No QUMOND field solve beyond the local phantom source and its monopole. The Cassini Q₂ of the patched law
  is still uncomputed.
- No SPARC fit of y_t.
- K8 uses the local constant-u balance. The neglected derivative terms are ≤ 2e-4 of the kept ones on the
  tested grid. It is not a full nonlinear BVP; A60 has one for the Sun.
- It does not rule out a turn-off from a UV completion or from a new coupling. It shows only that the present
  action (W, γ/L★, the linear clock term) cannot give one without a new constant.
