# ET2_free_core_low_mass: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** ET1 found S_need rising below V_flat 150 km/s (68.6, 102.7, 143.2 M☉/pc²) against route E's flat floor, but S_need there used M200 from the EM1 relation, and M200 × 0.5 moved the 20–60 bin enough to admit canonical's floor. Does the low-mass rise and the disagreement with the floor survive when no M200 is assumed? Standing: κ = ½ FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.

**Seen before freezing.** ET1's table, verdicts and M200 × 0.5 mutation, and the post-result Spearman +0.60 below lg M 10.5. No free-r₀ fit has been computed.

**Sample.** ET1's: Q ≤ 2, Inc ≥ 30°, bins 20–60, 60–100, 100–150 km/s are primary; 150–200, 200–250, 250–400 reported.

**Measurement.** Same core shape `B` and same weighted mse of log g as ET1, at fixed Υ_disk (bulge 1.4 Υ). Two free halo numbers per galaxy, S and r₀, with no M200: g_h = G π S r₀² B(R/r₀) / R². Grids: S as ET1 (121 log steps, 10 to 3000 M☉/pc²); r₀ 41 log steps, 0.1 to 100 kpc. Primary Υ 0.50; 0.40 and 0.60 reported. Galaxies at a grid end in either number are counted as censored and kept at that end.

**Weak-constraint guard, frozen now.** A galaxy counts as CONSTRAINED if the set of (S, r₀) grid points with mse within Δ = 1/N_eff of the minimum spans less than 0.5 dex in S, with N_eff the number of OK points. Primary statistic uses all galaxies; the same statistic on CONSTRAINED galaxies alone is reported beside it. If the two disagree on a verdict, the verdict is reported as GUARD-DEPENDENT.

**Statistic.** Median S per bin with 95 % bootstrap interval (20000 resamples, seed 20261030).

**Verdicts, primary Υ 0.50, for the three bins below 150 km/s.**
1. **Rise:** Spearman ρ of lg S on lg V_flat over V_flat < 150, permutation p (20000, same seed). RISE SURVIVES if ρ > 0 at p < 0.01; RISE GONE if p ≥ 0.01; FALLS if ρ < 0 at p < 0.01.
2. **Floor, per footing (106.85 canonical, 129.13 alt):** FLOOR HOLDS if all three intervals contain it. FLOOR REJECTED if at least two exclude it on the same side. MIXED otherwise.
3. **M200 dependence:** for each of the three bins, ET1 and ET2 agree if their intervals overlap. M200-INDEPENDENT if all three agree; else M200-DEPENDENT, listing bins.

**What each outcome means, declared now.** RISE SURVIVES with FLOOR REJECTED, M200-free, would count against the flat floor at low mass from rotation curves and the chosen core shape. RISE GONE means ET1's rise cannot be separated from its M200 relation or from free-fit degeneracy, and no statement about the floor follows from it. Free-fit S and r₀ are degenerate when curves end near r₀, so wide intervals mean no result, never a pass. Nothing here derives a parameter, and no fitted curve enters another lane without its own criteria.

**Checks.**
- K1: at S and r₀ taken from ET1's `solve_r0` for three galaxies, g_h equals ET1's `gh_of` to 1e-10.
- K2: synthetic galaxies with observed g set to baryons plus a planted (S, r₀) return both within one grid step: (50, 1), (200, 3), (800, 10).
- MUTATE (`--mutate`): each galaxy's observed g replaced by baryons plus a halo at flat S = 100 M☉/pc² with r₀ from ET1's M200, separate outputs. Exit 1 if verdict 1 returns RISE SURVIVES, so a flat truth does not read as a rise through the fit.

**Limits declared now.** One Υ for all galaxies; a chosen core shape; distance and inclination errors ignored; intervals cover sample scatter only; low-mass gas and asymmetric drift corrections as supplied by SPARC. Single-threaded, small job.
