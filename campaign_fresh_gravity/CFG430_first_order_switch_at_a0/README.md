# CFG430: does the LMP coexistence field h_c land on y = g_b/a0 = 1 from the operator itself?

**Verdict: CONDITIONAL under the frozen rules. In plain terms, this is not a derivation of the switch at a0.**

**What passes.** Take the kernel-Bose reading, in which ν(y) = Σ e^{−k√y} is read as one Bose mode with fugacity e^{−√y} (dictionary D1: e^{βh} = e^{−√y}). At the band onset (CFG481's own "phantom switch temperature"), the operator gives βh_c = −1.000 exactly for the pure cap. That is y_c = 1.000.
- The value is an exact identity. Onset sits where Kχ = 1, so βh_c(onset) = −6/(n_max + 2), which is −1 for the LMP cap n_max = 4.
- C1 passes: y_c = 1.000 at U = J = 0 for all three values of a.
- C2 passes: all 18 core settings fall inside the 0.1 dex window, with y_c from 0.815 to 1.012. The U = 0.1 rows sit near the lower edge.

**Why this is not a derivation.**
1. **It hinges on the integer cap.** n_max = 3 gives y_c = 1.44 and n_max = 5 gives 0.73.
2. **It hinges on the D1 reading.** Plain log-fugacity (D2) gives y_c = 0.37 for every setting (C4 fails).
3. **It holds only at the critical point, where the band has zero width.** The transition there is continuous, not first-order. Any real first-order band puts h_c above y = 1, since y_c = 4K² for U = J = 0. At the band CFG481 matched to CFG480 (γ = 6.25), y_c = 1.70–1.89: 0 of 18 settings inside the window (C3).
4. **a0 enters only as the unit of y inside the dictionary.** The operator contains no a0, G, ρ_Λ or κ. It supplies the number −1, from the cap and the Kac onset.

**PM cross-check (C5), which downgrades the result to CONDITIONAL.** On the two 256³ z = 0 snapshots (cfg424 FLAT alt seed360, cfg410 FLAT canonical), s_ph and s_c were recomputed with the CFG424 engine functions.
- The engine's own switch boundary, s_ph = s_c, fires at median y = 0.0013 and 0.0015.
- On the ON cells it fires at y = 0.008 and 0.005.
- The mesh never reaches y ≥ 0.5: the maximum is 0.023–0.029.

So the simulated switch lives about three decades below y = 1. These runs cannot test a y = 1 switch at all.

**MUTATE.** A planted βh_c = −1 (M1) reproduces C1 and C2 PASS. A planted −2 (M2) gives FAIL (y_c = 4). Both flip as required. The main run's C1 and C2 are numerically the M1 case, which is the point: the pass is the integer −1.

**Checks.**
- C0: I1 (h_c = X_s − (n_max/2)β²a) matches CFG481's own `scan_band` to 2.5e-10. It matches a symmetry-free Maxwell root at three settings.
- Runs 1–3 are kept as `*_runN_INVALID.out`. Run 1 had a wrong U coefficient in X_s. Runs 2–3 had check-harness bugs. Dated notes are in FROZEN_CRITERIA.md. The decision rules did not change.

**Caveats.**
- CFG481's transfer matrix counts the on-site U twice per site (2U·C(n,2)). This is harmless there, since U = 0, but its docstring understates U.
- CFG480's committed `.out` is a crash traceback. The 6.25 modal ratio lives in its JSON.

**Files.** `cfg430_hc_map.py` (`MUTATE` argument for the controls), `cfg430_hc_map.out`, `cfg430_hc_map_MUTATE.out`, `cfg430_results.json`, `cfg430_results_MUTATE.json`.
