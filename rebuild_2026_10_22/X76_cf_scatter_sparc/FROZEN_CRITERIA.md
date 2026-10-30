# X76_cf_scatter_sparc: FROZEN CRITERIA (committed alone, before any script or number)

**Why.** X48 FP1 (b275b44b8a) shows the mean peak builds no concentration. c_f is set entirely by the random small-scale
field, so it is a per-halo distribution: A3's nine ng 64 seeds give 2.44–15.09. X74 gives every SPARC galaxy one median
c_f. With A3's median (7.74), the canonical SPARC line fails on median Υ 0.48 (pre-read P2, flat 7.74: rms 0.0708, Υ 0.47).

The native model with its own scatter instead gives each galaxy its own c_f, drawn from the native distribution. This is
not a knob: the distribution is A3's committed per-seed set, used as measured. The owner said "keep swinging doors"
(10-29).

**Standing.** κ = ½ FITTED. Footings never pooled. Not theory closed. Nothing here may say the data favour the framework.
Cold dark energy is a gravitating field component, never a particle.

## Model (fixed now)
- X74's script and machinery, unchanged: X73 PRIMARY, shape S, native Ω_c/Ω_b, slope 2.7774, f★ 0.034. SPARC does not
  depend on f★; this is checked.
- The single change: each SPARC galaxy g gets η_g = η(c_g) = (4/(3 B_S(1))) c_g^{5/4}, with c_g drawn independently and
  uniformly from A3's nine ng 64 per-seed c_f values (`x48_analyze_results_ng64_A3.json`, 10¹², flag ok). It is flat in
  mass (no A4 is used), as in pre-read P2.
- Each galaxy keeps its own best-fit Υ (EM1 `fit_one`). The pooled statistic is EM1 `pooled`: rms, and median Υ over
  galaxies.
- **Draws:** 10 000 independent assignments (numpy default_rng seed 20261029). Each galaxy is fitted once per c value, and
  draws only re-index those fits.

## Verdict (per footing; canonical = headline)
- **P_line** = the fraction of draws that pass the SPARC line (rms ≤ 0.110 and median Υ in [0.50, 0.80]) on BOTH
  backgrounds (A_c2b_refit and B_cfg886_bg).
- **Labels:**
  - **SCATTER PASSES** if P_line ≥ 0.5;
  - **SCATTER FAILS** if P_line < 0.5.
  - Reported alongside: P_line, and the 16 / 50 / 84 % of median Υ and rms over draws.
- **Sensitivity (reported, not graded):** the pooled 18-realisation set (A2 ng 48 plus A3 ng 64). FP2 says the
  unresolved members are lower bounds.

## Checks (all must pass, else UNDECIDED)
- **K1:** every galaxy at c = 4 reproduces X73's committed PRIMARY SPARC numbers (rms, U_median, n_active) exactly, on
  both footings and both backgrounds.
- **K2:** every galaxy at c = 7.7395930714417345 reproduces pre-read P2's SPARC numbers exactly.
- **K3:** the base exec's own X74 K1 identity (c_f 4 vs X73) prints PASS.
- **MUTATE:** every c_g × 2 must lower the canonical median-of-draws Υ by more than 0.01.

## Not covered (stated now)
- The cluster keys and groups are not regraded with scatter. Cluster keys are stacks, and η ∝ c^{5/4} is convex, so
  scatter raises the stacked core mass at fixed median. A SCATTER PASSES here does not carry to clusters. That needs A4's
  per-seed sets.
- No retuning after the number. If it fails, it is reported with its mechanism.
