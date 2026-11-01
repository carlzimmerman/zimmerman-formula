# TP1_trough_predictor: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** Seven lanes chased the low Υ at 150–250 km/s under the response. Two things were never checked. Is that trough real against sampling, given 25 and 18 galaxies? And inside the sample, does a measured property separate the galaxies that need undoing from those that don't? If a mechanism such as bars, bulges or disc heating is behind it, it should show up per galaxy, without any fitted rule.

**Disclosed. Not blind.** Bin medians from UR2, ER1, SR1. Disc share at 2.2 R_d peaks at 150–200 km/s but contains V_obs, so it's excluded here. HS1 reported tilt with surface brightness, on another rule. No per-galaxy read of this statistic has been looked at.

**Expectation on record, mine.** Trough real at about 2σ, not overwhelming. Surface brightness is the likeliest predictor, because it carries baryon concentration. Distance method is a dull but possible cause, since Υ scales with distance. No clean bar proxy exists in SPARC's table: Hubble type T is a poor stand-in. Most likely reading: surface brightness only, which restates f_local.

## Data
UR1's path, NR1's η, EM1, δ 0, background A, with SPARC's quality cuts Q ≤ 2, i ≥ 30°. Per-galaxy Υ under Blumenthal, under off, and ΔΥ = Υ_off − Υ_Blum. Galaxies at the Υ grid's ends are kept and flagged.

## Tests
1. **Trough:** T = median Υ_Blum(150–250) − median Υ_Blum(of 100–150 and 250–400 pooled), bootstrap 95 %, 20,000 draws, seeded. **TROUGH REAL** if the interval excludes 0. Same for off.
2. **Predictors,** within 100–400 km/s, partial Spearman with Υ_Blum holding lg V_flat by linear residuals: lg SB_eff, lg SB_disk, lg R_disk, gas fraction 1.33 M_HI / (0.5 L + 1.33 M_HI), Hubble type T, bulge share of 3.6 µm mass from the rotmod files, distance. Seven tests. **PREDICTOR** needs permutation p < 0.05/7, 20,000 permutations, on the same residuals.
3. **Distance method:** median Υ_Blum by SPARC's f_D (Hubble flow vs the rest), within 100–400 km/s, reported.
4. **Forward, only for a named predictor:** does splitting at its median within 150–250 km/s give one half at Υ_Blum ≥ 0.50? Reported, no rule built.

None of these uses V_obs in a predictor, a₀, or a fit beyond the residual line.

## Labels
**TROUGH REAL / NOT DISTINCT**, and **PREDICTOR: name / NO PREDICTOR**. No mechanism is proven by a correlation. T is not a bar measurement.

## Checks
K1 per-galaxy medians by bin reproduce UR2's δ 0 rows, |d| ≤ 0.01. MUTATE: shuffled predictor gives p above the line; shuffled V_flat removes the trough.

Stop rule, mine, on record: this is the last lane of this push unless it names a predictor. After it, write up where the swing converged. κ = ½ FITTED, unused. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.
