# X64 assumption ledger (committed with FROZEN_CRITERIA.md, before any script or number of this lane)

κ = ½ FITTED. Footings never pooled. Cold dark energy is not matter and not a particle. Not "theory closed".

## Inputs and their class

| input | class | used for |
|---|---|---|
| X19's class table and per-member rows (rebuilt by X19's own code, read-only) | record (RAW / SURVEY-CALIBRATION / ΛCDM-PROCESSED per X19's ledger) | every non-lens class |
| X58's retention pattern (dwarfs retain, L* excluded, groups/clusters retain) | FRAMEWORK-NATIVE (record result) | labels |
| F2_outer_lensing inventory (`f2_outer_lensing_results.json`: weighted ⟨log M★⟩ per bin, h70, LePhare + 0.15) | SURVEY-CALIBRATION | KiDS lens class |
| F2/X53 lens cold-gas relation lg M_cold = lg M★ + (−0.69 lg M★,70 + 6.63) and hot gas 0.5 M★ within 100 kpc | record convention (F2 L4 central) | lens baryons |
| EM1 R1 relation lgM200 = 11.18 + 0.9 (lgM_b − 10), background A_c2b_refit (CLASS, read-only exec) | FRAMEWORK-NATIVE (route-E fit to SPARC) | C5 M200, EPS z_f, t(z) |
| X51 cooling-floor M200 per footing | FRAMEWORK-NATIVE | C5 for dwarfs |
| X53 bin-mean log M200 | FRAMEWORK-NATIVE | K4 only |
| t_H = 13.8 Gyr, μ = 0.6 | conventions (X19) | C3, C5 |

## Assumptions (named, so a reader can attack them)

- **A1 Labels are X58's pattern, not X19's E-labels.** X19 labelled by the measured extra against the isolated law. Here
  the label is the switch requirement from X58: the three dwarf classes the law under-predicts at Z ≥ 2 retain; groups
  and all three cluster terciles retain (as the brief states); the L* lenses, SPARC large and the MW disc are excluded
  (the law fits them; X53/X55 show route-E halos cannot fit SPARC and KiDS together). Groups and cluster T1 are fitted
  by the law too (X19), so labelling G drops them; W widens to every hosted system that needs no more than the law.
- **A2 KiDS lens class.** Four stellar-mass bins (F2 weighted ⟨log M★⟩), converted to the native h = 0.679 by
  + 2 log₁₀(0.70/0.679); the D_A ratio qDA (≈ 1) is neglected (disclosed). M_b(<r) = M★ + M_cold + 0.5 M★ min(1, (r/100
  kpc)³). Radius: X53's primary lensing range 0.035–0.31 Mpc; each bin enters at r = 0.035, 0.104 (geometric centre) and
  0.31 Mpc, so the class has 12 members and its 16–84 % range covers the radius choice. σ = V/√2 with V² = g r and
  g = the isolated law on g_N (per footing): lenses are law-following by label, and this is X19's rotator convention.
  Lens N, t_cross from the same r, σ. Reported variant: the single radius 0.104 Mpc.
- **A3 Radius reconstruction.** X19 does not store r per member. For every class except groups,
  r = 3 x a₀ / (4πG ρ_b) because X19 sets x = G M_b(<r)/(r² a₀) and ρ_b = M_b(<r)/(4/3 π r³) at the same r. Groups'
  x is the catalogue g_bar (not G(M/2)/R_e²), so groups take R_e from the Tian+26 table directly. K1 checks both.
- **A4 Internal potential.** Environment terms are removed (peer lane X62_environment_keyed_switch owns environment).
  The internal forms (§3 of the criteria) follow X19's own internal terms. Host-inclusive |Φ| is reported only.
- **A5 σ conventions.** X19's: σ_LOS (dispersion-supported), V/√2 (rotators), √(kT/μm_p) (clusters; finite KT only, so
  cluster members without KT drop from σ-based candidates, as in X19).
- **A6 Relaxation granularity.** m̄ = 0.5 M☉ for every class (a stellar mean mass). For gas-dominated clusters this
  overstates graininess; the ordering it gives is close to that of M_b · t_cross / ln N. Disclosed.
- **A7 Halo masses for C5.** EM1's relation is a route-E SPARC fit; applying it to lenses, groups and clusters is an
  extrapolation (K4 checks the lens end against X53). Dwarfs use X51's cooling-floor M200 (one value per footing), since
  EM1's relation runs far off its grid there; the extrapolated version is reported where on the EPS grid (lg M ≥ 7).
- **A8 C4 is reported only** (by-construction risk, X19 V8). C4L reduces identically to x (Σ_b/Σ_a₀ = 2x); it is kept to
  show the reduction, not as an independent key.
- **A9 Trials.** p_any by exact relabelling enumeration (class counts fixed). Its floor for any single perfectly ordered
  variable is 2/120 = 0.017 under P; with ~8 correlated candidates p_any can exceed 0.05 even if one separates — then
  the verdict is UNDECIDED (chance level), stated as such.
- **A10 Background.** The cosmic background is not placeable on M_b, σ, r-based candidates; its requirement (retain at
  background level so linear growth survives) is checked in step 4 (R1), not in the rank test.
- **A11 Radius heterogeneity.** As in X19, classes are compared at their own measurement radii. A key that separates
  only through the radius convention (e.g. lenses at 0.1 Mpc vs dwarfs at r_½) is a convention artefact risk; the
  lens-radius variant and the strict intervals are reported to expose it.
