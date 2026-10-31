# ET5_joint_upsilon_pressure: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** ET3: upper-bound pressure support softens the 20–60 km/s deficit. ET4: a Υ trend softens the 100–150 excess. Neither alone explains the rise. Together, with the beam cut, do they reconcile the real curves with route E's flat floor? Standing: κ = ½ FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.

**Seen before freezing.** ET2, ET3, ET4 tables, each change alone, plus ET3's WORST cell without a trend. No cell combining a trend with pressure support has been computed. Those tables make it likely that some cells contain the floor, so this rule demands both conditions below.

**Base.** ET2's sample, core, grids, mse. Rise statistic, intervals and floors (106.85, 129.13) as ET3. Trend Υ = 0.50 (V_flat / 80)^s and yardstick as ET4: s = 0.25 is the largest counted as allowed. Pressure g_obs + σ²/h, h = Rdisk, an upper bound that can overcorrect, as ET3. Beam cut R ≥ FWHM × D, fewer than 5 OK points dropped, as ET3.

**Part 1, real curves, full grid.** s ∈ {0, 0.25, 0.5}, σ ∈ {0, 8, 12} km/s, FWHM ∈ {0, 30″}: 18 cells.

**Verdict per footing, from the cells.** A cell is RECONCILED if all three intervals contain the floor **and** the rise has p ≥ 0.01.
- **JOINT EXPLAINS IT** if any cell with s ≤ 0.25 is RECONCILED.
- **JOINT EXPLAINS IT ONLY BEYOND THE BAND** if only s = 0.5 cells are.
- **FLOOR CONSISTENT, RISE REMAINS** if a cell with s ≤ 0.25 has all intervals containing the floor but every such cell has p < 0.01.
- **NOT RECONCILED** otherwise.

Searching 18 cells with upper-bound corrections favours reconciliation, on purpose. A pass here therefore shows that known systematics can absorb the rise at their most generous; it does not show that they do. A NOT RECONCILED carries more weight for the same reason. Wide intervals containing the floor are absence of evidence, so the p condition is required, and p ≥ 0.01 alone is not evidence of flatness.

**Part 2, forward.** Truth flat at each footing's floor with r₀ from ET1's M200; truth Υ trend s ∈ {0.25, 0.5}; observational σ ∈ {8, 12}; FWHM ∈ {0, 30″}: 8 cells per footing. Fit at Υ 0.50 with no correction, as ET2 fitted the real data. FAKED / PARTIAL / NOT FAKED by ET3's rule. Reported per footing as the worst cell, separately for s = 0.25 and s = 0.5.

**Reading, declared now.** JOINT EXPLAINS IT with a FAKED forward cell at s = 0.25: ET1–ET3's rise is not to be used against the floor. NOT RECONCILED and no FAKED: the rise stands against the flat floor given these systematics and this core shape, which identifies no mechanism and is not a rejection of route E. Mixed outcomes are reported as they fall. The two footings are never pooled, and the core shape stays untested here.

**Checks.**
- K1: s 0, σ 0, no cut equals ET2's S per galaxy.
- K2: s 0.25 alone reproduces ET4 Test 1's ρ and bin medians; σ 12 alone and 30″ alone reproduce ET3's P12 and B30 to 1e-9.
- MUTATE (`--mutate`): forward data, canonical floor, truth s 0.25, σ 12, no beam, fit with that exact trend and correction, separate outputs: medians within one grid step of the floor's neighbours (98–118) and p ≥ 0.01, or exit 1.

**Limits declared now.** h = Rdisk for all galaxies, while gas discs are longer. Beams bracketed, not per galaxy. 1D forward beam. Trend has one parameter, no colour data. σ constant across mass and radius. One core shape. Single-threaded, small job.
