# S2_v3_lowg_lensing AMENDMENT A1 (POST-RESULT; append-only; no pass/fail line, input, threshold or reading changed)

Written after the first scored run, whose verdicts and K6 FAIL had been seen.

1. **K6 stays FAIL as frozen, and the run exits 1 because of it.** The premise of K6, that the window amplitude A rises
   monotonically with y_e, is false at the 0.1 % level.
   - Six cells dip from y_e = 0 to the primary field (red R1/R2 and all R2, both footings). The largest is
     dA = −0.0028 = 0.058 σ_A.
   - Why: ΔΣ(R) = Σ̄(<R) − Σ(R) is a differential quantity. An external field that cuts the phantom off beyond
     r_e = r_M/x_e removes something close to a uniform sheet at R ≪ r_e, and a sheet does not change ΔΣ.
   - The remaining steepening raises ΔΣ slightly. For a point mass, ΔΣ(EFE)/ΔΣ(isolated) is 1.0016 / 1.0035 / 1.0059 at
     R = 10 / 15 / 20 r_M (canonical, primary field). It only falls below 1 near r_e: 0.968 at 30 r_M, 0.801 at 40 r_M.
   - Consequence for the frozen FAIL line ("short at y_e = 0, hence at every y_e"): the inference holds to ≤ 0.06 σ_A.
     No central verdict uses it, because the central verdicts are PASS and CONDITIONAL. The reported y_e scan
     (1e-6 … 3e-4) shows no class change on the grid.
2. **Memory.** The first run peaked at 1.18 GB RSS, which is over the 1 GB budget. Two causes: the memory-mapped KiDS FITS
   pages, and unchunked per-lens temporaries.
   - The code now reads the FITS columns in row chunks straight from the file, after asserting that none of those columns
     is scaled. It stacks the per-lens model in chunks of 20,000 lenses.
   - No equation, input, threshold or verdict line changed. The `.out` numbers were compared line by line with the first
     run: only timings, RSS and the A1 lines differ.
3. **Post-result reported-only lines added:** the size of the K6 departures and the point-mass ΔΣ ratio table above
   (`A1_K6_departures`, `A1_DS_ratio_point_mass` in the JSON); a listing of the P2 lane. P2 holds criteria and a script
   only and has no result files, so nothing was read from it.
4. **The u−r 2.5 colour variant (frozen as reported-only) is degenerate in this colour system.** It gives 1,432 red lenses
   out of 181,477. LePhare MAG_ABS colours are offset from B21's system, where the valley sits at 2.5; here it sits at 2.0,
   which is the record's `typ`. K5 confirms the `typ` split: record stack / B21 colour bins 1.071 (blue) and 1.053 (red),
   against 1.78 / 1.44 for the 2.5 split. The variant rows carry no information.
