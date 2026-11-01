# HL2_combined_mass_pairs: FROZEN CRITERIA (committed alone, before any new catalogue is fetched)

**Question.** HL1 read the gap log(M_WL/M_hydro) as +0.069 ± 0.043 on 50 clusters, NOT POWERED. With every usable published sample, each cluster counted once, is the gap there and how large?

**Standing.** κ = ½ FITTED. Cold dark energy, never a particle. Not "theory closed". Nothing here says the data favour the framework. No a₀, no footing.

**A bracket, never a framework grade.** Published masses are model fits on published distances. All LITERATURE-INPUT. This cannot say which mass is right.

## Sources
Mahdavi+13 (on disk). To fetch, as named: LoCuSS (Smith+16 hydrostatic bias; Martino+14; Okabe & Smith 16; Zhang+10), CCCP (Hoekstra+15), Weighing the Giants (Applegate+14, Mantz+16, von der Linden+14), CoMaLit (Sereno & Ettori 15). The same search may add a sample only if it tabulates both masses per cluster, and the lane lists it and every source rejected, with the reason.

**Inclusion, one rule:** a table gives, per cluster, M_WL and M_hydro at Δ = 500, from one paper or from two papers on the same cluster with radii within 10 % (M_hydro's radius the source's own). No Planck or SZ mass as M_hydro. No masses from a scaling relation.

## One count per cluster
Match across sources by position within 3′ and |Δz| ≤ 0.02, names as fallback. Each cluster's log(M_WL/M_hydro) is the unweighted mean over its source pairs. Split components stay as tabulated.

## Statistic, classes
- **g** = median over unique clusters; SE by cluster bootstrap, 5,000 draws, seed 20261031.
- Classes as in HL1, line 0.12: **NOT POWERED** SE > 0.04; **NO GAP** |g| ≤ 2 SE; **GAP AS LARGE** g > 2 SE and |g − 0.12| ≤ 2 SE; **GAP SMALLER** g > 2 SE and g + 2 SE < 0.12; **GAP LARGER** g − 2 SE > 0.12; **REVERSED** g < −2 SE.
- **[SOURCE-DEPENDENT]:** dropping any one source changes the class.
- **[OFFSET-DEPENDENT]:** HL1's ±0.014 on Mahdavi's M_WL changes the class.

Mahdavi enters through HL1's AMENDMENT_A1, which isn't accepted yet. Headline carries that condition.

## Reported, not graded
g per source. Mean, rms. Gas fraction log Y on each mass where M_gas is tabulated at that radius, f★ 0.034, 0.0615. A redshift split and an X-ray-mass split: M_hydro's noise pushes g the opposite way to M_WL's, so both splits are shown and neither is a mass trend on its own.

## Checks
- **K1, per source:** M against 500 ρ_c(z)(4π/3) r³ at the source's own stated cosmology where a radius is tabulated: signed offset ≤ 5 %, 16–84 % width ≤ 3 %. Failing sources are dropped and listed.
- **K2:** rows accounted for, every skip listed.
- **K3:** Mahdavi's clusters alone reproduce HL1's g exactly.
- **K4:** on clusters in two sources, the same mass agrees: median |difference| reported, and a source differing by > 0.1 dex in median is flagged.
- **MUTATE:** swap flips g exactly; shuffling M_hydro raises rms.
- K2 or K3 failure: no verdict, exit 1.
