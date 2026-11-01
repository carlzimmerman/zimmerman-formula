# TP1_trough_predictor: TROUGH REAL, NO PREDICTOR. The 150–250 km/s trough survives sampling; no measured property without V_obs separates the galaxies inside it. Half of them pin at the Υ grid's floor. This ends the push, by the stop rule on record

Criteria: `FROZEN_CRITERIA.md` (e22feda417), committed alone first. `tp1.py`, `tp1_tail_add.py`, `tp1_read.py`, `tp1.out`, `tp1_results.json`. UR1's path, NR1's η, EM1, δ 0, background A. κ = ½ FITTED, unused. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.

**Trough** (median Υ, 150–250 against 100–150 + 250–400, 95 %): Blumenthal −0.160 [−0.220, −0.040]; off −0.250 [−0.490, −0.120]. **TROUGH REAL**, and present with no response, so the response deepens something already there. As Υ is capped, this is a lower bound on the gap.

**Predictors,** 100–400 km/s, n 76, partial Spearman at fixed lg V_flat, line p < 0.0071:
| lg SB_eff | lg SB_disk | lg R_disk | gas fraction | T | bulge share | distance |
|---|---|---|---|---|---|---|
| −0.251 (p 0.028) | −0.116 (0.32) | −0.177 (0.12) | +0.104 (0.37) | +0.138 (0.24) | +0.005 (0.97) | −0.100 (0.39) |

**NO PREDICTOR.** Surface brightness has the right sign and misses the line, as expected. Bulge share shows nothing. Distance method: 0.38, 0.40, 0.34, 0.32, 0.36, no clear effect, small n in places. T isn't a bar measurement, so **bars are untested, not excluded.** This sample has n 76 and a censored statistic, so a modest effect could be hidden.

**A limit I hadn't flagged earlier: the Υ grid's floor is 0.30.** 21 of 43 galaxies at 150–250 km/s and 46 of 123 overall sit at or below it under Blumenthal. So medians quoted as 0.30 in UR1, UR2, NR3, GT1 and SR1 are censored, and the true value may be lower. This doesn't help any rule. ER1's f_req at Υ 0.50 is read above the floor, so it stands. Rank tests here have ties.

## Where this push converged (UR1–UR3, SL1, SL2, ER1, GT1, SR1, SR2, TP1)
Established:
1. One adiabatic response gives the sign flip between discs and cluster cores, with no new number. Its amplitude fails.
2. Lighter halos can't fix it (UR2). Energy at one coupling has the wrong order (ER1). Symbolic search found no a₀-free hit (SL1). The note's gates fail on their own terms or on holdouts (GT1, SR2).
3. The Milky Way asks for about 4 × 10¹⁰ M☉ cold inside R₀; DiskMass, if its σ_z stands, for most of the contraction kept; SPARC at 150–250 km/s for most of it undone. These overlap in mass, and no property tested separates them.

Not established: η and core shape from first principles; the cause of the trough; whether DiskMass's σ_z stands; whether the smooth core is right inside 10 kpc, since it starts × 2.7 below the zoom's own shape at R₀.

Decisive next data, none on this machine: a bar classification for SPARC galaxies, and an old-population σ_z for DiskMass-like discs. Neither is a new formula, and both can come out against the framework.

## Checks
K1 bins reproduce UR2's δ 0. MUTATE shuffled V_flat +0.010 [−0.160, +0.140]; shuffled SB −0.047.
