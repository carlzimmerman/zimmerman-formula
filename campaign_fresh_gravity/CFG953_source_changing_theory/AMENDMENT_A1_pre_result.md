# CFG953 AMENDMENT A1 (2026-10-21, PRE-RESULT for the main stage)

Written after the criteria commit (049a0f867) and after the K stage (all K pass), while the MUTATE stage was running. Written before
the main stage had produced any number. Committed alone. No pass line, test, variant or class rule changes.

## A1.1 A reported-only diagnostic added to (g): the host body inside an in-situ system

**What the frozen (g) leaves out.** The frozen (g) grades SCT-M's prediction for in-situ systems as plain Newton of their own baryons
(f = 0), which is CFG936's route (i) statistic. That is the right reading of "no own body". But an in-situ system also sits inside
its parent's smooth spherical body. The body is part of the parent, and it reaches the in-situ system as an external tidal field
whose trace part is the parent body's local density ρ_h. Averaged over orientations, the in-plane radial pull this adds at radius r
is (4π/3) G ρ_h r. Neither CFG936 nor the frozen (g) includes it. The record's own routes ignore the host's local density in the same
way.

**What is added (reported, no class weight).**
- **Class T (TDGs).**
  - Host: CFG936's convention, M_h = 0.6 L_K at D = D_p (projected, so a lower bound on the 3-D distance and an upper bound on
    ρ_h).
  - ρ_h is the SCT-M body density of a point-mass host (simple kernel, census supply), set to zero beyond the host's own edge.
  - Δ = log10(1 + (4π/3) G ρ_h R_out / g_bar), with g_bar = 10^lgbar from CFG936's per-object values. The shifted residuals
    r − Δ are scored with CFG936's statistic.
- **Class U (DF2 / DF4).**
  - ρ_h is the sum of the bodies of NGC 1052 (1e11 M⊙) and NGC 1035 (5e9 M⊙) at CFG936's printed projected distances
    (DF2: 79.3 / 219.5 kpc; DF4: 165.3 / 21.0 kpc), each set to zero beyond its own edge.
  - M_* and R_e are from CFG939's table (DF2 2.0e8 M⊙ / 2.0 kpc; DF4 1.5e8 M⊙ / 1.6 kpc). r = 1.305 R_e and M_b(<r) = M_*/2.
  - Δ ln σ² = ln(1 + (4π/3) ρ_h r³ / M_b(<r)), and the shifted residuals are scored.
- This is an estimate of the term's size only. Orientation, 3-D distances and host masses are not known well enough for a grade.
- The frozen grade of (g) is unchanged: it uses f = 0 Newton, as frozen.

## A1.2 Order of runs

The MUTATE stage started before this amendment existed. A1.1 adds code to the main stage only. K and MUTATE will be rerun from the
final script after the main run, and their outputs compared with the first ones (disclosed in DERIVATION).

κ = ½ FITTED; footings never pooled; cold energy, no particle species; not theory closed.
