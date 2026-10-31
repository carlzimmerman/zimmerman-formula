# ET3_low_mass_systematics: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** ET2 found free-fit S rising with V_flat below 150 km/s (70.2, 107.7, 157.5 M☉/pc²; ρ +0.556), and showed shuffled residuals do not fake it. Shuffling cannot test errors that vary smoothly with radius. Can beam smearing, pressure support, inclination or distance errors, or sample quality remove the rise, or produce it from a flat floor? Standing: κ = ½ FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.

**Seen before freezing.** ET1 and ET2 tables, verdicts and post-result diagnostics. None of the variations below has been computed.

**Base.** ET2's sample, core shape, grids, mse and Υ 0.50 (bulge 1.4 Υ). Spearman ρ of lg S on lg V_flat for V_flat < 150 km/s, permutation p (20000, seed 20261030). Medians and 95 % intervals as ET2. S, r₀ from the free grid fit. D, e_D, Inc, e_Inc, Rdisk, Q from `SPARC_Lelli2016c.mrt`. The per-galaxy HI beam is not in that table, so beams are bracketed at 15″ and 30″ FWHM, a choice stated here.

**Part 1: real curves, each change alone.**
- B15, B30: drop points with R < FWHM × D. A galaxy left with fewer than 5 OK points is dropped and counted.
- P8, P12: pressure support, g_obs → g_obs + σ²/h with σ = 8, 12 km/s and h = Rdisk. Short h makes this an upper bound, and some SPARC curves may already carry a correction, so this can overcorrect. It lifts low-mass curves most, so it works against the rise.
- I45: keep Inc ≥ 45°.
- Q1: keep Q = 1.
- MC: 20 draws, each galaxy i ~ N(Inc, e_Inc), floored at 15° and capped at 89°, with g_obs × (sin²Inc / sin²i), and D ~ lognormal with fractional sd e_D/D: R × f, g_obs / f, g_bar unchanged. Seed 20261030.
- WORST: B30 + P12 + I45 + Q1 together.

**Verdict 1, RISE:** ROBUST if B15, B30, P8, P12, I45, Q1 each give ρ > 0 at p < 0.01 and at least 19 of 20 MC draws do. ROBUST-BUT-WORST-LOST adds that WORST does not, and is the reading when only WORST fails. FRAGILE lists any other failure. WORST is reported with its surviving n; below 30 galaxies under 150 km/s it reads UNDERPOWERED and cannot fail the rise.

**Verdict 2, FLOOR per footing (106.85, 129.13):** each variation's three bins below 150 km/s, graded by ET2's rule (HOLDS, REJECTED, MIXED). Reported as a table. STABLE if all variations give one verdict, else VARIATION-DEPENDENT.

**Part 2: forward model, can systematics fake the rise?** Truth: every galaxy has flat S at the footing's floor, r₀ from ET1's M200, baryons at Υ 0.50. Observed curve: true V on a fine radial grid from baryons interpolated in R and the halo; V odd through R = 0; 1D Gaussian smoothing along R with FWHM × D; then g_obs = V²/R − σ²/h at the real points. Cases: F15 (15″), F30 (30″), F30P8, F30P12 (with no correction applied). Refit S and r₀.

**Verdict 3, per footing, per case:** FAKED if ρ > 0 at p < 0.01 and the 20–60 median ≤ 77.3 and the 100–150 median ≥ 136.6 (ET2's interval edges). PARTIAL if ρ > 0 at p < 0.01 only. NOT FAKED otherwise. The verdict on the rise as a whole is the worst case over footings. Any FAKED means ET2's rise cannot be read as physics from these data. 1D smoothing is not a 3D beam model; a NOT FAKED is conditional on that.

**What each outcome means, declared now.** ROBUST and NOT FAKED: the rise is not explained by the systematics tested, which counts against a flat floor at low mass within the chosen core shape, and is not proof of a mechanism. FRAGILE or FAKED: ET1 and ET2's low-mass rise is not to be used against the floor. Either is reported the same way. No parameter is derived, and no curve enters another lane.

**Checks.**
- K1: zero change reproduces ET2's S per galaxy exactly.
- K2: on-grid plants at three (S, r₀) return exactly. ET2's off-grid K2 failure is why plants are on grid here, disclosed.
- K3: forward model with FWHM 0 and σ 0 returns g_obs equal to the truth at real points within 1e-3 in log g, and refits within one grid step in S for the median galaxy.
- K4: smoothing lowers V at R < FWHM × D on a rising curve.
- MUTATE (`--mutate`): truth S ∝ V_flat^1 normalised to 100 at 80 km/s, no systematics, separate outputs: must read ρ > 0 at p < 0.01, or exit 1. This confirms the pipeline can see a real rise.

**Limits declared now.** Beam sizes bracketed, not per galaxy. No warps, non-circular motions or 3D beam. One Υ. The core shape is chosen. Single-threaded, small job.
