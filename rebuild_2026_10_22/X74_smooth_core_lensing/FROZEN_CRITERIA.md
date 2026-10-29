# X74_smooth_core_lensing: FROZEN CRITERIA (committed alone, before any script or graded number)

**Question.** X73 regraded the X43 line set (SPARC, groups, 15 cluster keys) with the smooth core and every input
measured or native, and the canonical footing passed. It did not regrade galaxy lensing. X53 (Brouwer+21 KiDS-1000
isolated lenses, 4 bins, full covariance) found **OUTER LENSING DISCRIMINATES: LAW** against route E's Burkert halos:
Δχ²(H2H − L2H) +429.6 canonical and +455.6 alt (all radii), and +133.1 / +144.5 at R ≤ 0.31 Mpc. Most of that came from
halo mass normalisation, not shape (AMENDMENT A1). Does X70/X73's smooth core change that grade?

## Change (one, nothing fitted)

X53's script, unchanged except for the halo shape:
- Burkert B(x) → smooth B_S(x) = 4(asinh x − x/√(1+x²)), ρ ∝ (1+x²)^{−3/2};
- η(M) → η(M)·B1/B_S(1), X70's re-derivation, giving η = 10.82 at c_f = 4.

M200 still comes from EM1's SPARC relation, the core Σ = max(Σ_a0, ηΣ_coll), and the halo is still truncated at R200.
Lens baryons are F2's inventory, unchanged. X73's measured f★ and gas tail are cluster inputs and do not enter galaxy
lenses.

## Pre-registered expectation (written before any number)

M200 is fixed at R200 and the gap is normalisation, so I expect the smooth core to move Δχ²(H2H − L2H) by less than 20
on all radii, and the class to stay LAW on both footings.

## Identity and MUTATE (stop rule: identity FAIL → no verdict)

- **K1.** With the shape switch on Burkert, the script reproduces X53's committed `x53_outer_lensing_results.json`
  χ² values (L, H, L2H, H2H; primary and all; both footings) to 1e-9.
- **K2.** The smooth B_S closed form matches quadrature to 1e-6, and B_S(1) = 0.69707.
- **MUTATE.** X53's own mutate (truncation at 100 R200) under the smooth shape must change H2H χ².

## Verdict (X53's frozen class rule, applied unchanged, per footing)

X53's thresholds on Δχ²(H2H − L2H), all radii, with 2h: LAW / HALOS / NOT DISCRIMINATING, plus its systematics-dominance
test. Reported for each footing:
- **SHAPE MOVES THE LENSING GRADE** if the class differs from X53's;
- **SHAPE DOES NOT MOVE THE LENSING GRADE** otherwise.

The size of the change, |Δχ²_smooth − Δχ²_Burkert|, is reported against the pre-registered 20.

**Reported only:** primary-range Δχ²; the X48 ng48 c_f, z_eff R200 and background-B variants; AMENDMENT A1's
common-shift profile under the smooth shape (the best shift in log M200 and the Δχ² there).

κ = ½ FITTED; c_f EXTERNAL; footings never pooled; cold dark energy is a gravitating field component, never a particle;
not theory closed; nothing here says the data favour the framework. One thread, nice 15.
