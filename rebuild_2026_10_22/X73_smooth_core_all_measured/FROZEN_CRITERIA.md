# X73_smooth_core_all_measured: FROZEN CRITERIA (committed alone, before any script or graded number)

**Question.** X70_smooth_core_shape's canonical full pass and X71's single break (G-OUT-M3 UNDER, Z 2.25–2.33 at
h 0.672) were both graded with two inherited inputs:

- the Planck dark-to-baryon ratio 5.364 and H0 = 67.4 in X30's prep (`Mfair=5.364*Mbt`, `OC946 = 5.364*OB946`);
- X30's "P" gas tail, with no measured slope beyond R500.

GS1_measured_gas_outskirts graded the native normalisation with the measured X-COP slope (s = 2.777) counted to the
self-consistent r_ta. It used Burkert and kept f★ = 0.20. **No lane has graded the smooth core with every input measured
or native at once.** This lane does that. Nothing is fitted.

## Configuration (PRIMARY, nothing free)

- **Core:** X70's smooth core ρ0/(1+x²)^{3/2}, η = 10.82 (X70 PRIMARY), c_f = 4 (EXTERNAL, unchanged).
- **Normalisation:** native, as GS1/GC2: Ω_c/Ω_b = (Ω_m − Ω_b)/Ω_b from h 0.6856427, Ω_m 0.2976016, ω_b 0.0223081, in
  place of 5.364 and H0 67.4.
- **Gas tail:** GC2's extension with the "R5" switch point and slope s_meas = 2.7774 (GS1 committed), counted to the
  self-consistent r_ta.
- **Stars:** Mb = Mg·(1 + f★) inside R500 **and** in the tail (GC2's hard-coded 1.2 becomes 1 + f★). f★ uniform over
  all clusters, stars following the gas (as X71 / CFG408).
- **Graded f★ (both graded, neither preferred):** F-A1 = 0.034 (CFG408 PRIMARY), F-XC = 0.0615 (X-COP-7 median).

## Identity checks (stop rule: any FAIL → no verdict)

- **K1.** Burkert, f★ 0.20, native + tail at s_meas reproduces GS1 `runs/x43copy_R4_meas_results.json` cluster preds,
  every key, both footings, both h cells, to 1e-9.
- **K2.** Smooth, f★ 0.20, inherited, no tail reproduces X70 `x70_smooth_core_results.json` cluster preds to 1e-9.
- **K3.** Smooth, f★ 0.034, inherited, no tail reproduces X71 `x71_results_fs0.034_S.json` cluster preds to 1e-9.
- **MUTATE.** f★ = 0.60 in the PRIMARY configuration must raise G-OUT-M3's pred above the f★ = 0.20 run.

## Verdict (frozen, per footing, never pooled)

- **ALL-MEASURED PASSES:** in both graded f★ variants, all 15 cluster keys |Z| ≤ 2 in both h cells, groups |Z| ≤ 2, and
  the SPARC line passes.
- **ALL-MEASURED BREAKS: <lines, sign, f★ variant>:** otherwise; every failing line is named.
- **Robustness:** the same grade at GS1's bootstrap slopes s16 = 2.6756 and s84 = 3.0711. ROBUST if the class is
  unchanged at both edges; otherwise FRAGILE.

## Reported only (not graded)

- f★ 0.20 in the PRIMARY configuration (isolates the f★ effect);
- Burkert (X43, η 14.8) at both measured f★ in the PRIMARY configuration (the GS1 comparison);
- smooth, measured f★, native but no tail; and smooth, measured f★, tail but inherited (which input moves G-OUT-M3);
- G-OUT-M3, G-OUT-all and G-IN-Mall Z for every run.

## Scope and disclosures (frozen)

- A pass is scoped to the X43 line set. KiDS lensing (X53) and the dwarfs (X51) are not regraded.
- The tail is extrapolated from x_max ≈ 1.5–2.1 R500 to r_ta (as GS1).
- Stars following the gas puts more stellar mass at large radius than a BCG-dominated profile; at f★ ≤ 0.06 this is
  disclosed, not corrected.
- κ = ½ FITTED; c_f EXTERNAL; footings never pooled; cold dark energy is a gravitating field component, never a particle;
  not theory closed; nothing here says the data favour the framework.
- One thread, nice 15, under 1 GB per run (X48 A4 zooms are live).
