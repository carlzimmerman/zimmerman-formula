# CFG303 — Addendum 1 to the frozen criteria (52976ec22), written before any replaced input was evaluated

**What had been seen when this was written:**
- the committed CFG223 script re-run unmodified in the scratch mirror. Its results JSON is identical to the committed one, and its .out differs only in the run-time line;
- the RC100 Table 3 columns 5–8 (δ log SFR(MS), log M★, log M_baryon, log M_bulge), transcribed into `rc100_table3_cols5to8_transcribed.csv` from the three rendered table images of the local PDF;
- a pre-check of gates T1 and T2 when that file was written. Both pass: all 100 log M_baryon cells equal the corrected CSV, the 7 bulge cells equal the committed CSV's mistaken values, and the names and redshifts agree in every row;
- the source of CFG213 (its BINS loop and reported extras), CFG216, CFG217's `mu_t18`, CFG220's `rows_for` and `vec_rows`, and the layout of CRISTAL's vector summary, where for disc 02 `table_Rout` is 8.10 kpc against the outermost data marker at 7.47 kpc.

No native g_bar, D, δ or s* had been computed.

## A1.1 CRISTAL at R_out: which radius is "inside the data"
The frozen R2 text describes the R_out velocity as "at the outermost data radius". CFG223's committed R_out points use the vector summary's `table_Rout` row. That radius can lie beyond the last plotted data marker (02: 8.10 against 7.47 kpc), where the model curve, halo included, is an extrapolation.
- **Native primary at R_out:** the `outermost_data_marker` radius definition (inside the data; the velocity there is MODEL-OTHER, `halo_in_fit = yes`).
- **Also reported:** the `table_Rout` variant, matching CFG223's radius, labelled "model curve at or beyond the last marker".
- **Controls:** C-i and C-ii at R_out use `table_Rout`, because that is what CFG223 committed.

## A1.2 CFG213's Z5 bin, natively
CFG213's recorded statement ("the rival is disfavoured on the fit route only") is re-run on native rows. The procedure:
- exec CFG213's committed source through its BINS loop, so that its bootstrap state is the committed one;
- C-ii checks that the loop's results equal the committed `cfg213_two_sided_results.json` entries;
- evaluate the native Z5 rows with CFG213's own `deltas`, `med_ci` and `verdict`, at α = 3.36 and α = 1.68 (g_obs = (V_rot² + α σ₀²)/R_e), for both kernels and both footings;
- apply CFG213's robust-verdict rule (one verdict across α ∈ {3.36, 1.68} × kernels × footings).

The native rows are the twelve primary discs restricted to finite log M★ and f_molgas, with g_bar = M★/(1 − f_molgas) × `disc_v2(1, R_e, R_e)`/R_e.

## A1.3 RC100 sample B binning
Sample B is all 100 galaxies. It uses CFG223's committed quartile edges (computed from the committed table's z, which equals the corrected table's z) and CFG223's own bin rule. A pooled point is added. Sample A (the RC41 overlap) uses the same edges, with a pooled point.

## A1.4 MUTATE scope
C-iii, as frozen, is applied to every native CFG223 point. For the CFG216 slopes and the S5 inversion it is applied as the log D shift check, with the slope shifts reported and not graded, because a uniform mass shift moves a slope only through the kernel's curvature.

KURVS (R4) specifics will be fixed in Addendum 2, after its pipeline has been read and before its run.
