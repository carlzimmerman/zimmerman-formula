# ET4_upsilon_trend: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** ET2 and ET3 fit one Υ for all galaxies and found S rising with V_flat below 150 km/s (70.2, 107.7, 157.5 M☉/pc²). Can Υ changing with mass explain that rise? Standing: κ = ½ FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.

**Seen before freezing.** ET1, ET2, ET3 tables, including S at Υ 0.40, 0.50, 0.60 by bin, where 20–60 barely moves. None of the tests below has been computed.

**Base.** ET2's sample, core, grids and mse; bulge 1.4 Υ. Rise statistic and intervals as ET3: Spearman ρ of lg S on lg V_flat, V_flat < 150 km/s, permutation p (20000, seed 20261030). Trend family: Υ = 0.50 (V_flat / 80 km/s)^s, nearest value on the 0.01 grid, clipped to the grid's ends and clips counted. Across 20–150 km/s the trend changes Υ by 0.88 s dex.

**Allowed band, a declared yardstick.** ±0.11 dex about 0.50, Υ 0.39–0.64, the galaxy-to-galaxy scatter usually adopted for [3.6]. It is used as a yardstick, not derived here and not measured on this sample. So s = 0.25 (0.22 dex end to end, the full width of the band) is the largest trend counted as allowed; s = 0.5 and 1 are reported as beyond it.

**Test 1, real curves with a trend.** s = 0.25, 0.5, 1. ERASED at s if p ≥ 0.01, else SURVIVES. Floor graded per footing by ET2's rule.

**Test 2, Υ-insensitive galaxies.** f★ = Σ Υ A / Σ |g_bar| over OK points at Υ 0.50, where g_bar = G + Υ A is split using its exact linearity in Υ. Below 150 km/s: GAS group f★ < 0.5, STAR group f★ ≥ 0.5. Rise statistic in each at Υ 0.50. For GAS: fewer than 20 galaxies reads UNDERPOWERED; otherwise RISE WITHOUT Υ LEVER if ρ > 0 at p < 0.01, else NO RISE IN GAS GROUP. The group sizes and V_flat ranges are reported, since a narrower range lowers power. As a sensitivity, the GAS group is repeated at Υ 0.30 and 0.80.

**Test 3, needed Υ.** Per footing: S fixed at the floor (106.85, 129.13), minimise over the Υ grid and the r₀ grid per galaxy. Median needed Υ per bin with 95 % interval; galaxies at a Υ end counted. IN BAND if all three medians lie in 0.39–0.64, else OUT, listing bins. Also reported: median ratio of best mse at the floor with free Υ to best mse with free S at Υ 0.50.

**Test 4, forward.** Truth: flat S at the footing's floor, r₀ from ET1's M200, Υ by the trend at s = 0.25, 0.5, 1. Fit at Υ 0.50 with free S, r₀. FAKED / PARTIAL / NOT FAKED by ET3's rule (ρ > 0 at p < 0.01; 20–60 median ≤ 77.3 and 100–150 median ≥ 136.6).

**Overall verdict, frozen.**
- **Υ EXPLAINS IT** only if at s = 0.25 Test 1 is ERASED and Test 4 is FAKED on at least one footing, and Test 3 is IN BAND for that footing, and Test 2 is not RISE WITHOUT Υ LEVER.
- **Υ COULD EXPLAIN IT ONLY BEYOND THE BAND** if the first two hold only at s = 0.5 or 1, and Test 2 is not RISE WITHOUT Υ LEVER.
- **NOT EXPLAINED BY Υ** otherwise. This covers Υ alone only. It does not rule out Υ together with ET3's systematics, which is why the floor table is reported, and it says nothing on core shape.

**Checks.**
- K1: s = 0 reproduces ET2's S per galaxy exactly.
- K2: G + Υ A rebuilt from Υ 0.40 and 0.80 equals g_bar at Υ 0.60 to 1e-10 relative on OK points, all galaxies.
- K3: planted (Υ on grid, S and r₀ on grid) in Test 3's search at free S returns them exactly on three galaxies.
- MUTATE (`--mutate`): forward data with truth s = 0.5, fit with the correct trend, separate outputs: must read p ≥ 0.01, or exit 1. Exit 1 also if the same data fit at Υ 0.50 has a smaller ρ than the correct-trend fit, since a trend left unmodelled should tilt S upward.

**Limits declared now.** The trend is a one-parameter power law in V_flat; no colour or age information. Band is a yardstick. Gas masses taken as given, with no molecular or helium variation beyond the base. One core shape. Single-threaded, small job.
