# CFG215 — the decomposition δ(z) timeline (four samples, z ≈ 0.3–5.7)

- **Criteria:** `FROZEN_CRITERIA.md` (f5950bd4b), committed before any number. **κ = ½ FITTED, NOT DERIVED.** These are author decompositions, not a direct a₀ measurement.
- **Run:** `python3 campaign_fresh_gravity/CFG215_decomposition_timeline/cfg215_timeline.py`, about 6 s. It passes 4/4 checks. `MUTATE=1` (RC41 D × 1.5) passes 5/5.
- **Chart:** `cfg215_delta_vs_z.png`, drawn by `cfg215_plot.py` from the lane's own pipeline.
- **Statistic:** δ = log₁₀(D_obs/ν(g_bar/a₀,L)) at R_e, from each sample's own disc–halo decomposition.
  - Flat a₀ against the rival a₀ × E(z); ν_mono, canonical footing decides.
  - The primary series uses only anchored or independent routes. The fit-route series is separate and never pooled.

## Bottom line

- **No law fits all four samples in the primary series (T1).**
  - **Flat:** MUSE-DARK DISFAVOURED-under (−0.157 [−0.293, −0.072]); RC41 DISFAVOURED-over (+0.102 [+0.058, +0.145]); NOEMA3D and CRISTAL CONSISTENT.
  - **Rival:** MUSE-DARK DISFAVOURED-under (−0.249 [−0.356, −0.173]); RC41, NOEMA3D and CRISTAL CONSISTENT (+0.017, −0.011, −0.198 [−0.321, +0.107]).
- **No trend claim is possible (T2).**
  - The across-sample slopes are +0.13 [−0.00, +0.36] per unit z for flat and +0.06 [−0.05, +0.34] for the rival, so no significant across-sample trend.
  - Within MUSE-DARK the slopes are −0.18 [−0.40, +0.04] for flat and **−0.28 [−0.49, −0.06] for the rival**. Within RC41 they are +0.01 [−0.07, +0.08] and −0.05 [−0.11, +0.03].
- **The route-mixing mock declares the across-sample slope NON-DIAGNOSTIC BY CONSTRUCTION.**
  - Route biases b_s = median log₁₀(M_ind/M_fit): MUSE-DARK +0.512, RC41 +0.051, NOEMA3D +0.048, CRISTAL +0.044.
  - The rival's signal slope, with flat exactly true and no bias, is only −0.032 per unit z. The mock "truth = independent" on the fit-route series gives −0.095 for the rival, i.e. 2.9 times the signal.
  - The frozen rule (mock ≥ 50% of the signal) is therefore met, whatever the data give. The per-sample verdicts remain informative; the slope across samples does not.

## The per-sample story (primary series unless noted)

| sample | n | z | flat | rival |
|---|---|---|---|---|
| MUSE-DARK, SED + main-sequence H₂ | 109 | 0.86 | −0.157, under | −0.249, under |
| MUSE-DARK, DC14-fitted (fit route) | 109 | 0.86 | +0.047, consistent | −0.038, consistent |
| RC41, prior-anchored fit | 41 | 1.50 | **+0.102, over** | +0.017, consistent |
| NOEMA3D, SED + measured CO | 10 | 1.24 | +0.046, consistent | −0.011, consistent |
| CRISTAL, SED + dust gas | 9 | 5.23 | +0.043, consistent | −0.198, consistent |
| CRISTAL, fit route | 12 | 5.19 | +0.053, over | −0.161, **under** |

- **RC41 is the one sample where the flat law is disfavoured on the anchored route.**
  - It is +0.102 [+0.058, +0.145], robustly across every kernel and footing.
  - The rival is consistent in 3 of 4 cells there.
  - With the SED + gas route variant (the total held fixed) both are consistent: flat +0.048 [−0.095, +0.129], rival −0.084 [−0.190, +0.019].
  - So the RC41 result is route-dependent too.
  - Post hoc, applying the geometry factor ×0.844 anyway leaves flat at +0.090 [+0.037, +0.126].
- **MUSE-DARK's independent route disfavours BOTH laws (under),** because its SED + H₂ baryons run 0.51 dex heavier than the DC14 fit. This is the mass-route problem of CFG198/199 again. Post hoc, the result holds without the 4 near-zero-rotation galaxies (flat −0.148, rival −0.227) and gets stronger under reading (a) (flat −0.271, rival −0.345).

## Controls

- **C1.** A synthetic galaxy placed on each law returns δ = 0 exactly.
- **C2, the calibration gate (reported).** The median model/table V_bary² ratio over the 22 NOEMA3D and CRISTAL decompositions is **1.185** (range 0.88–1.55), inside [0.8, 1.25]. So RC41 enters as is.
- **C3a.** CRISTAL's and NOEMA3D's per-sample medians equal CFG213's committed medians to 1e-9, in every cell.
- **C3b.** CFG199's reading-(b) lowest-z-third median log₁₀ a₀ = −10.1435 is reproduced.

## Fix after the first run (kept)

- The first run crashed in the mock: `brentq`'s bracket [−12, 14] in log y did not contain the root for MUSE-DARK ID 1119. Its model velocity at R_e is about 2 × 10⁻¹⁰ km/s, so g_obs/a₀ ≈ 10⁻²³.
- The bracket was widened to [−80, 14]. No other change was made.
- The crashed log is kept as `cfg215_timeline_firstrun_crashed.out`. Its printed numbers up to the crash are identical to the final run's.
- **Four MUSE-DARK galaxies (v_perp(R_e) < 10 km/s) are near-zero-rotation models.** They stay in the frozen sample, and the post hoc row shows they change nothing.

## Limitations

- Four samples of different fitting codes (GalPaK3D, DysmalPy), priors and pressure prescriptions. There is no cross-sample correction, and the samples are never pooled.
- RC41's g_bar comes from my disc + bulge geometry (R_e,bulge 1 kpc declared) at one radius.
- All four use MAP fit values. The fits' own posterior widths are not propagated.
- Nothing here says the data favour the framework. The flat law is disfavoured in two of four samples on the primary series, and the rival in one.

## Correction after CFG216's cross-check (appended 2026-09-29; the text above is unchanged)

- **RC41's flat verdict is geometry-sensitive.** CFG216 (`../CFG216_rc100_within_sample/`) found 38 of the 41 RC41 galaxies in RC100 by name.
  - For them, the median of [δ_flat from RC100's own V_c and f_DM − δ_flat from this lane's disc + bulge geometry] is −0.042 dex (range −0.35 to +0.03).
  - On RC100's own V_c and f_DM, the RC41 subset gives δ_flat +0.041 [+0.004, +0.109], not this lane's +0.102 [+0.058, +0.145].
  - So "flat DISFAVOURED-over at RC41, robust in all four cells" should read "borderline: +0.04 to +0.10, depending on whether g_bar comes from the fit's velocities or from a disc + bulge geometry".
- **What stands:**
  - the route-mixing mock's NON-DIAGNOSTIC verdict for the across-sample slope;
  - the other samples' numbers.
- **T1 is unchanged in form:** no law fits all four samples, since MUSE-DARK's independent route disfavours both.
