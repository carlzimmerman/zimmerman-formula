# LS1_lstar_analogs: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** Route E's Milky Way falls about 20 km/s short at the solar circle inside its priors (X79). Is that the Milky
Way, or every galaxy of that kind? SPARC's line grades the sample median Υ, and each galaxy has its own Υ, so a deficit in
massive spirals could be hidden by a high per-galaxy Υ. Idea relayed from an external model; thresholds below are its
proposal, fixed here unchanged. Standing: κ = ½ FITTED; footings never pooled; not theory closed.

**Sample (from `SPARC_Lelli2016c.mrt`, not SPARC_table.txt).** V_flat in [200, 250] km/s, Q ≤ 2, Inc ≥ 30°. Control: same
cuts with V_flat in [100, 150] km/s. Fewer than 5 analogs: UNDECIDED.

**Model.** X73 PRIMARY halos, exactly as X76's `fits()`: X74 base exec, f★ 0.034, slope 2.7774, background A_c2b_refit,
existing `fit_one`, Υ grid and bulge convention unchanged. Graded at c_f 4 (the only configuration that passes). Reported,
not graded: CE1's converged η 25.94 at 10¹², as c_f-equivalent 8.05.

**Statistics, per footing.**
1. Median best-fit Υ of the analogs.
2. ΔV = median over analogs of [mean over points with 2 ≤ R/R_d ≤ 4 of (V_model − V_obs)], at Υ_disk fixed to 0.50.
   Galaxies with no point in that range are excluded and counted.

**Verdict (headline canonical; alt reported separately, its SPARC line already fails per X78).**
- **SYSTEMATIC L★ DEFICIT:** median Υ > 0.80 OR ΔV < −15 km/s.
- **MILKY WAY IS THE OUTLIER:** median Υ in [0.50, 0.70] AND |ΔV| ≤ 10 km/s.
- **MIXED:** anything else.

**Checks.**
- K1: all galaxies at c_f 4 reproduce X73's committed SPARC rms and median Υ exactly.
- K2: a synthetic galaxy whose V_obs equals its own model at Υ 0.50 returns ΔV = 0 to 1e-6.
- MUTATE: halo mass × 0.5 must make ΔV more negative.

**Limits declared now.** One Υ value is a choice: stellar-population Υ has real scatter, and massive spirals may differ. Rotation
curves are not the Milky Way's Jeans curve. A MILKY WAY IS THE OUTLIER result does not fix the Milky Way; it only says where to look.
