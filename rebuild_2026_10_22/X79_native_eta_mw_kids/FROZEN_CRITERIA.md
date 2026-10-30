# X79_native_eta_mw_kids: FROZEN CRITERIA (committed alone, before any script or graded number)

**Question (owner, 10-29: "Yes, grade them").** X77 measured the collapse coefficient directly from the native zoom halos:
η_native = 20.83 at 1e12 (ng 64), 13.79 at 1e13 and 14.39 at 1e14 (ng 48). This is the "c_f falls with mass" table.
With route E's core rule Σ = max(Σ_a0, η_native(M) Σ_coll(M)) and the smooth core, do the Milky Way and KiDS-1000
galaxy lensing pass?

**The rule (both parts):**
- η_native(M) is X77's three medians (`x77_results.json` summary, keys 1e+12_ng64, 1e+13_ng48, 1e+14_ng48),
  interpolated linearly in lg M and held flat outside.
- Σ_coll(M) is X43's committed table, interpolated as in X53.
- Smooth core B_S. Footings are never pooled.

## Part MW (GD3's stage-M machinery, read-only, exec'd from its own text)
- Change: GD3's `grade()` gets Σ from the rule above, using GD3's own M200 (EM1 R1 relation on each cell's baryon mass),
  in place of OS1's σ law. Nothing else changes: X5's 175-cell box, the McMillan row, the lines L1 / L2a / L2b / L3, the
  classes (FEASIBLE IN PRIORS / FEASIBLE (WIDE PRIORS ONLY) / V+K ONLY / INFEASIBLE) and D.
- **Graded:** canonical and alt, background A, PRIMARY key.
  - SPARC gate from X77's full grade: canonical line PASS; alt line FAIL (Υ 0.45). So alt's class carries
    "SPARC LINE FAILS (MW reported)".
- **K1 identity:** with Σ from OS1's law at GD3's q_fS, the harness reproduces GD3's graded classes and best D to 1e-9.
- **Reported:** constant η 10.82 (c_f 4); the McMillan row; Σ/Σ_a0 and the rule state (floor or collapse) at the MW mass.

## Part KiDS (X74_smooth_core_lensing's patch of X53, exec'd from text)
- Change: X53's `eta_of(M, "cf4")` returns η_native(M) in place of 10.82. Nothing else changes: X53's halo masses,
  truncation, 2-halo term, covariance and verdict rule.
- **Graded:** X53's verdict per footing, and Δχ²(H2H − L2H) on all radii, compared with X74_smooth_core_lensing's
  +423.7 / +458.4.
- **K2 identity:** with η ≡ 10.82, the χ² values reproduce X74_smooth_core_lensing's committed results to 1e-9.

## Rules
- **MUTATE:** η_native × 2. The MW best-D Σ ratio must rise, and the KiDS H2H χ² must change by more than 1.
- No retuning after the number. A4's ng-64 cluster η replaces the ng-48 entries in a rerun only; it is not a new
  choice.

κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework. Cold dark energy is a gravitating
field component, never a particle.
