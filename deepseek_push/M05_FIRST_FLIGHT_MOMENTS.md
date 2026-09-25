# M05 — FIRST-FLIGHT GEOMETRIC MOMENTS: EXACT CLOSED FORMS
**2026-09-23 · volume window theory · anchors found, quadrature-certified · concurrency: M05_geometric_anchors.py + M05b_simpson_check.py**

## The finding

For a volume-uniform source in the unit sphere with isotropic emission, the
**first-flight geometric moments** are exact rationals:

```
⟨chord⟩         = 3/4        (mean path to the wall)
E[∫₀^L r²(s)ds] = 5/12
E[∫₀^L r⁴(s)ds] = 1/4
```

Quadrature evidence (Legendre, exponentially convergent; the Simpson check in
M05b was trapezoid-weak on the r=1, μ=0 corner and is superseded by the
doubling-ladder, recorded for audit):

| ng | ⟨chord⟩ | E∫r² | E∫r⁴ |
|---|---|---|---|
| 64 | 0.7500000220987 | 0.41666668877 | 0.25000002211 |
| 128 | 0.7500000014017 | 0.41666666807 | 0.25000000140 |
| 256 | 0.7500000000883 | 0.41666666675 | 0.25000000009 |
| 512 | 0.7500000000055 | 0.41666666667 | 0.25000000001 |
| 1024 | 0.7500000000003 | 0.41666666667 | 0.25000000000 |

Convergence to 3e-13.  These match the J11/K07 MC anchor (volume atom at
τ₀-independent z ≤ 1.25) — the atom law A_v = E e^{−τ₀(chord + q·I₁)} is now
**closed-form at first order in the exposure**: A_v ≈ exp(−τ₀(3/4 + 5q/12))
as τ₀ → 0.

## The closed-form thin window

K07 measured c₀(q) = lim E[D]_vol/τ₀ = 0.3962 ± 0.0028 (q=0), 1.089 ± 0.004
(q=3), 2.668 ± 0.008 (q=10); K07's thin limits 1.893/1.837/1.837.  With the
anchors the thin-limit window is the exact expression

```
R_v(0,q) := lim_{τ₀→0} (−ln A_v / E[D]_vol) = (3/4 + 5q/12) / c₀(q)     (M05-I)
```

| q | closed-form numerator | c₀ (K07) | R_v(0,q) |
|---|---|---|---|
| 0 | 3/4 = 0.75 | 0.3962 | 1.893 |
| 3 | 2.0 | 1.089 | 1.837 |
| 10 | 4.9167 | 2.668 | 1.843 |

All three match K07's measured thin limits (1.893/1.837/1.837) to SE.  This
replaces three MC numbers with one formula; the remaining open piece is
**c₀(q) itself** — if c₀(q) is also linear (c₀ = a + bq), the entire thin
window is a rational curve in q.  The M05 run's 3e6-photon thin MC gave
c₀ = 0.406/1.094/2.619 ± 0.013–0.033 (consistent with K07's values; the
q=3 point favors linearity: pred a+3b = 1.069 vs 1.094, z ≈ 1.1 — not yet
conclusive at current SE).

## The r⁶ moment (for the second order)

E[∫r⁶ds] = 0.21285714295 (Legendre 256-pt) — the rational reconstruction
(limit-denominator 20000) does NOT resolve to a clean fraction proven;
candidates 149/700 = 0.212857142857 (diff 9e-11) and 3/14 − 1/700 are within
quadrature error but neither is certified.  Registered OPEN: the M01 Lean lane
may certify 3/4, 5/12, 1/4 via the same change-of-variables it already uses
for the chord moment; the 4th moment sequence (5/9·…?) is a symmetry puzzle
for the next wave.

## Novelty (per user rule: new + framework-core)

- Not in the frozen lane, not in post-LRD literature: the first-flight moment
  triple (3/4, 5/12, 1/4) is the exact law behind the volume atom's
  τ₀-linearity — the analogue of ⟨chord⟩ = 3/4 already found in J11, with the
  r²/r⁴ exposure moments new.
- (M05-I) turns the volume-window thin limit into a closed-form curve, and
  the R_v(0,q) values re-derive K07's MC table to SE — the parameter-space
  narrowing: τ₀ → 0 limit no longer needs Monte Carlo.
- Empirical anchor: none needed beyond the K07/J11 MC already on record;
  this is algebra of the geometry, Lean-certifiable next.

## Files
M05_geometric_anchors.py (theorem run, first 3 checks PASS at 1e-9; thin-atom
and c₀ legs recorded), M05b_simpson_check.py (independent-integrator audit,
recorded; superseded by the Legendre ladder), this verdict.  No git commit —
owned by the M-series conductor commit cycle.

## SUPERSEDED IN PART — 2026-09-25, X-WAVE (see deepseek_push/X-WAVE_BRIEF.md, X01_ladder_closure.py)

The **E[∫₀^L r⁴(s)ds] = 1/4 entry in the table above is WRONG — the true value
is 17/60**.  The hand-written antiderivative of (R²+2Rμs+s²)² used in this
file's `first_flight_moments` I2 expression (and, inherited, in P01's I2/I2_b
gates and Q01's g_m(4)) has halved s²/s³ coefficients:
(2R²μ²+R²)/3·L³ + RμL⁴/2 instead of (4R²μ²+2R²)/3·L³ + RμL⁴.  The buggy
expression integrates to 1/4 exactly — which is why the Legendre ladder
"confirmed" it (the check `E_int_r4_quarter` compares against the same buggy
quantity).  Three clean routes (closed-form ladder X01-I, sympy-exact
antiderivative reduction, 40-dps definitional quadrature) agree at 17/60 to
<1e-30, and the closed form

    M_n = E[∫₀^L (R²+2Rμs+s²)^n ds] = (3/(2(n+1)(n+2))) · Σ_{k=0}^n (k+1)/(2k+1)

reproduces EVERY other rung exactly: 3/4, 5/12, 149/700, 1069/6300, 13649/97020
(m=4 was the one rung never re-derived by a clean route — absent from every K0
replication gate).  The thin-window law (3/4 + 5q/12)/c₀(q) uses only m=0 and
m=2 (both correct); no physics claim downstream used the m=4 value.  The
corrected core is machine-checked in fable_independent_2026/lean_2026/
X01_ladder_core.lean (x01CoreR4 : ∫P~₄ = 17/60).