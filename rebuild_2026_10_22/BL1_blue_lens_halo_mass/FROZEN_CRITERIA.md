# BL1_blue_lens_halo_mass: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** X55 found that route E's SPARC halo-mass relation sits about 0.4 dex below what KiDS isolated lenses want. SPARC is a sample of late-type discs. KiDS's isolated stack at log M★ ≈ 10.8 is mostly red. S2 already shows, in the law's case, that blue and red lenses at fixed M★ differ (A 0.878 vs 1.313, canonical). Is the mass gap the same for blue lenses, the population SPARC actually samples, or is it a colour split?

**Method.** S2's forward model, read-only: 181,477 B21 isolated lenses, per-lens weights, S2's central config (native h, Ω_m, inventory baryons, hot CGM 0.5 M★ to 100 kpc), GLS amplitude A = data / model in CFG829's window (g_bar 10^−13.3–10^−11.9, 6 B21 points). S2's central colour split is used; the u − r 2.5 split is reported. Only the model changes.

**Model (route E, Newtonian, no EFE).** M(<r) = M_b(r) + M_h(r), with:
- M200 from EM1's relation, background A, at log(M★ + M_cold), as in X53.
- Core rule: FC1's S_cold (commit 061b2e2a1a), floor at each footing's Σ_a0, smooth core.
- **Graded profile E (extended):** the smooth core normalised to M200 at R200, continued to r_ta = (3 (M200 + M_b) / (4π · 5.55 · ρ̄_m,0))^(1/3) / (1 + z), with z the lens-weighted median of the sample. Halos do not stop at R200 in any route E picture, and clusters already use r_ta.
- **Reported profile T (truncated):** cut at R200, X53's choice.

No two-halo term. The window ends near 400 kpc for typical lenses, and S2's law reference also has none.

## Frozen grades, canonical and alt separately, on profile E at EM1's M200 (Δ = 0)
Using S2's `cls_amp`:
- **BLUE CONSISTENT:** |A_blue − 1| ≤ 2σ.
- **BLUE BETWEEN:** 2σ–3σ.
- **BLUE SHORT:** A_blue − 1 > 3σ (data above route E).
- **BLUE OVER:** 1 − A_blue > 3σ.

Colour reading, also frozen. Δ_c is the common shift in log M200 giving A = 1 in class c, from a grid of −0.4 to +0.8 in steps of 0.05, interpolated. Its 1σ range comes from A ± σ_A.
- **COLOUR SPLIT:** Δ_blue's 2σ range contains 0 and Δ_red's does not.
- **GAP IN BOTH:** neither 2σ range contains 0.
- **NO GAP:** both contain 0.
- **OTHER:** anything else, stated.

## Reported, not graded
Profile T at Δ = 0; the law's A in the same run; χ² over all 15 bins; u − r 2.5 split; f★-free statement of M200 multiples relative to R_nat for each class.

## Checks (any failure makes the verdict NOT DECIDED)
- **K1:** S2's own table call reproduces its committed L4 A values (blue, red, all, both footings) to 1e-6.
- **K2:** M_h(R200) = M200 to 1e-8 at three masses.
- **K3:** the smooth-core solve at S = 106.85 M☉/pc² and M200 = 1e12 agrees with X43's closed form to 1e-6.
- **MUTATE:** halo × 0.5 must raise A_blue.

## What this cannot show
- Blue lens masses have their own M★ scale errors. The grade quotes A with statistics only. CFG926's and CFG667's corrections are about red masses; the blue offset is not measured here.
- Selection: photo-z isolation leakage is not modelled (X53's caveat) and it raises all classes.
- A colour split would not derive why red lenses are heavier, and it would be a new requirement on the halo rule, not a pass of route E.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework.
