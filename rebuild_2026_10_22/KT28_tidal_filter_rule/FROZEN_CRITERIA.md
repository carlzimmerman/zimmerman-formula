# KT28_tidal_filter_rule — FROZEN CRITERIA (before any script; only the two hand estimates below were computed)

Owner, 2026-11-03: KT27 killed the local rule ξ = |g|²/(|∇g| g*) at the dwarfs. Fornax was lost because the rule sees the
Milky Way's uniform field. Try a different rule that can't see a uniform field.

**Post hoc, on the record:** this rule was proposed after seeing KT27's Fornax fail. It's the second local-rule attempt
(KT26/27 was the first) and is registered as such. Labels and lines are KT25's/KT27's, unchanged.

κ = 1/2 FITTED, held fixed. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. No
download.

## The rule
Equivalence principle: a uniform field is undetectable locally, and only the tidal tensor T = ∇∇Φ is. So build the length from
T alone. In the spherical, row-wise form used here, with g(r) the system's own field:
  τ(r) = sqrt(g'² + 2 (g/r)²)   (Frobenius norm of T for a radial field)
  **ξ_tid(r) = (4/√3) τ³ / (|dτ/dr|² g*)**, g* = a0 / κ.
The factor 4/√3 is fixed by the deep-MOND point mass (g = V∞²/r gives ξ_tid = V∞²/g* = κ r_M exactly), set before any data.
|∇T| is reduced to the radial derivative of τ (spherical approximation, stated). A uniform external field adds nothing to T,
so only the system's own field enters. In KT15/KT16's quadrature EFE models that's g_int = ν(sqrt(g_N² + g_e²)/a0) g_N. Newtonian
point mass: ξ_tid = (4√2/9) g_N r / g*.

## Tests (both footings graded), as KT27 except for the rule
- **T0 Milky Way:** KT26's code, MW filter length = ξ_tid(R0) from the observed curve (V 229.1 km/s, dV/dR -1.7 km/s/kpc,
  V linear in R, so V'' = 0), one value per footing, 1375 in-prior cells, lines L1, L2a, L2b, L3. Pass if ≥ 1 cell passes all
  four. In-plane spherical form; the vertical tidal component (dominated by the local disc density) isn't included, stated.
- **T1 Cassini:** KT16's integral, ξ_tid(x) row-wise from g_int. Pass if Q2 ≤ 5.2e-27 s^-2.
- **T2 dwarfs:** KT15's model, smoothing row-wise at ξ_tid(r) from g_int. Pass if ≥ 15/24.
- **T3 SPARC:** KT19's code, ξ_tid(R) row-wise from the board-law curve at f = 1. Because τ' needs a second derivative of an
  interpolated mass profile, ln τ is smoothed with a Gaussian of width 0.1 in ln r before differentiating, for SPARC only.
  Pass if d rms ≤ 0.005 and |median| ≤ 0.05.

Clips and the small-width mask as in KT27 (ξ ≤ 200 kpc or 1e4 r_M; width below 3 grid steps means unsmoothed).

**Label per footing: TIDAL RULE SURVIVES** if T0-T3 all pass; **TIDAL RULE FAILS: <tests>** otherwise.

## Expectation on record, not blind (hand estimates, computed before freezing)
- ξ_tid(R0) = 8.78 kpc canonical, 7.26 kpc alt. KT26's 8.10 kpc failed canonical's MW and 6.71 passed alt's, and KT17's ε = 1
  (about 10-11 kpc) failed both. So **T0 canonical very likely FAILS; alt is open**.
- Cassini: with the external field the Sun's own field is near Newtonian times ν(η), so ξ_tid(r_M) ≈ 0.41 r_M (canonical)
  and 0.43 r_M (alt), falling as 1/r outward. KT16's constant-ξ thresholds are 0.45 and 0.50 r_M. So **T1 is at risk on
  both footings**.
- Dwarfs: MW satellites should now get about the isolated value (KT27: ξ ≈ 2.4 x r_M/2 at r = a), so Fornax may come back.

## Checks
- R1: forcing ξ to the constant 0.5 r_M reproduces KT25/KT27's rows (Cassini 0.4806/1.057, dwarfs 15/24, SPARC +0.0021/-0.0006).
- R2: ξ_tid / (κ r_M) for the board-law point mass at 100 r_M equals 1 within 1e-2 (the simple ν isn't exactly deep at
  100 r_M; the 1e-2 tolerance is set here, before running).
- R3: the SPARC smoothing of ln τ, applied to an analytic Plummer field, changes the median ξ_tid by ≤ 5 %.
- MUTATE: ν = 1; Cassini Q2 must be 0, SPARC must fail.
