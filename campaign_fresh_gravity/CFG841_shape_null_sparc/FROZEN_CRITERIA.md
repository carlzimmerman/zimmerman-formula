# CFG841 FROZEN CRITERIA: the calibration-free shape test of the law's form on SPARC (committed before any script)

**Source of the idea.** Codex's analytic review (`real_research/analytic_review_2026_10_18_codex/SHAPE_NULL.md`, candidate
test ZAR-D1): with q = V²/R, a gas template h and z = q²/h, the framework's **simple action law** g² − b g = a0 b
(canonical S2: g_N = g²/(g + a0)) predicts z = α q + β, while the rival **quadratic a0-line** g² − b² = a0 b predicts
z = α h + β (α, β > 0). Distance, inclination normalisation, a0 and the common gas conversion all cancel. No SPARC value was
used to set anything below.

## Sample (fixed before any residual is seen)
- SPARC rotmod files (`real_research/data/sparc_data/`), galaxy cuts Q ≤ 2, Inc ≥ 30° (`SPARC_Lelli2016c.mrt`); point cut
  errV/Vobs < 0.10 and Vgas > 0.
- **Primary (gas-only template):** points where the stellar share of g_bar (Υ_disk 0.5, Υ_bul 0.7) is ≤ 0.20; galaxies with
  ≥ 4 such points. h = Vgas|Vgas|/R.
- **Secondary (fixed-composition template):** all galaxies with ≥ 5 points, h = full g_bar at Υ 0.5/0.7 (approximation:
  composition varies with radius in reality; declared).

## Fit and statistic
- Per galaxy, weighted least squares of the residual r = z − (α x + β), x = q (simple) or h (quadratic), with errors from
  errV only (independent; declared limitation: no radial covariance available) plus a 3% floor on V:
  σ_r = |∂r/∂V| σ_V, where ∂r/∂V = (2q/h − α)(2V/R) for the simple model and (2q/h)(2V/R) for the quadratic. Iterate the
  simple-model weights 5 times.
- Δχ²_gal = χ²_quadratic − χ²_simple (> 0 favours the simple law). A fit is "physical" if α > 0 and β > 0.

## Classes (primary sample)
- **NOT DIAGNOSTIC** if fewer than 5 galaxies, OR if the power control (below) fails.
- **SIMPLE FAVOURED** if ΣΔχ² ≥ +9, more than half the galaxies have Δχ² > 0, and ≥ half the simple fits are physical.
- **QUADRATIC FAVOURED** if ΣΔχ² ≤ −9, more than half have Δχ² < 0, and ≥ half the quadratic fits are physical.
- **NEITHER** otherwise. The secondary sample is reported with the same classes, labelled approximate.

## Controls (power; run before reading the class)
- **MUTATE-S:** replace every Vobs by the simple law's prediction from that galaxy's own h (Q = λ = 1, canonical a0) plus
  Gaussian noise at the point's σ_V (seed 841). Must class SIMPLE FAVOURED.
- **MUTATE-Q:** the same with the quadratic law. Must class QUADRATIC FAVOURED.
- If either mutate fails, the real-data class is NOT DIAGNOSTIC (the data lack the leverage), whatever ΣΔχ² says.
- K1: the hand example of SHAPE_NULL.md (q = 1, 2, 3; h = 1/2, 4/3, 9/4) gives D_s = 0 and D_q = 1/12.

κ = ½ fitted (it cancels here); cold energy mass required; not theory closed. The test checks the law's algebraic shape, not
its dark-energy normalisation.
