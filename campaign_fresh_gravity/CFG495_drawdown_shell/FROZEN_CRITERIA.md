# CFG495 FROZEN CRITERIA: the cold-fluid drawdown around every halo, and its KiDS lensing test

Committed alone, after Steps 1 and 2 (simulation and prediction) and BEFORE the KiDS shear signal is read (Step 3).
Step 2 read only the lens catalogue and the KiDS pair weights, which are needed to pair-average a model into the 15 bins. It did not read the tangential-shear sums.
On-disk data only. κ = ½ is fitted. The cold mass is still required. Both footings (9.3603e-11 / 1.1312e-10) are scored separately and never pooled.

## The idea (owner-approved 2026-10-08)
The zero-knob growth rule (CFG424 engine, RC = 0) conserves mass halo by halo. The phantom excess e inside each halo's edge is drawn from the cold fluid in that halo's turnaround catchment, in proportion to the local cold density (comp = q·s_c, with q = Σe/Σs_c per catchment). So every halo should carry a DRAWDOWN: depleted cold fluid out to r_ta. ΛCDM (NFW + two-halo) and MOND (no cold fluid) do not make this prediction.

**Modelling choice, stated up front.** The engine spreads the draw over the whole catchment (proportional), including inside the edge. The outer-shell-only draw is a reported variant only.

## Step 1 result, declared (cfg495_sim.py + cfg495_sim_analysis.py; 512³ seeds 360/359, canonical + alt; 256³ checks)
- **Controls.** The engine's own q_max is reproduced to < 1e-6 (K1). Per-catchment mass conservation holds (K2). The peak catalogue reproduces the engine's catchment and edge masks exactly (K3).
- **Shell depletion, groups** (log M_ta 13.2–14.2 Msun/h, 512³). The cold-fluid depletion depth in r_edge < r < r_ta is **0.08–0.17**; for clusters (log M_ta ≥ 14.2) it is 0.30. The depletion does **not** end at r_ta: it stays at 0.08–0.15 out to 2 r_ta, because neighbours' catchments overlap.
- **Effective density (particles + e − comp) against the matched S0 control.**
  - Deficit of −4 to −11% at 0.25–0.65 r_ta (one bin +4%), −3 to −5% at 0.85 r_ta, and −1 to −3% at 1–2 r_ta.
  - Excess (+5 to +22%) in the edge cell.
  - Clusters: excess out to about r_ta, and a −4 to −6% deficit at 1.4–1.7 r_ta.
- **ΔΣ, TA total − S0, groups.** −0.03 to −0.26 h Msun/pc² at 0.45–1 r_ta (−1 to −7% of S0); clusters +5 to +12%.
- **ΔΣ of the drawdown alone** (with vs without the draw, same snapshot): −9 to −12% of S0 over 0.3–1 r_ta for groups, −26% for clusters.
- **Resolution.** The mesh does NOT resolve the drawdown amplitude. The median per-host q is 0.03–0.13 at 512³, against the continuum engine rule's 0.53–0.62 at the same masses (cfg495_lenslib.group_q). The edge is about one 0.39 Mpc/h cell. The mass-weighted q rises from 0.10 (256³) to 0.16–0.18 (512³).
  - The simulated amplitude is therefore a lower bound.
  - Mesh/continuum depth ratio in the lowest mass bin: **A_sim = 0.13–0.16** (reported only).
- **The outer-shell-only variant overdraws:** q_sh > 1 in 2–14% of catchment mass at 512³.
- **No KiDS-mass halos are resolved** (r_ON ≥ 1.56 Mpc/h means M_ta ≥ 1.7e13 Msun/h). In the engine, galaxy halos carry no drawdown at all, so the galaxy prediction is the engine rule written for one lens (Step 2).

## Step 2 prediction, declared (cfg495_predict.py, cfg495_lenslib.py)
**Per lens.** The lens has M_gal, z and log M*.
- The LCDM-equivalent matter is an NFW profile, with M200c from Moster+13 (z-dependent) and c from Duffy+08. **(U): these literature relations are recalled, not read from disk.**
- r_ta: the mean density inside it is (1+δ_ta(z)) ρ̄_m (CFG100).
- f_ret = M_gal/(f_b M_ta).
- r_edge = r_M / ln(1 + f_ret f_b/(1−f_b)), capped at r_ta.
- ρ_c = (1−f_b) ρ_NFW.
- ρ_ph comes from the ν_mono law of M_gal.

**Models:**
- **LCDM:** M_gal + (1 − f_b f_ret) ρ_NFW, out to r_ta.
- **F_nodd:** M_gal + f_b(1−f_ret) ρ_NFW + [r<r_edge] max(ρ_ph, ρ_c) + [r_edge<r<r_ta] ρ_c. This is the engine with the draw off.
- **PROP (the prediction):** −q ρ_c on r < r_ta, with q = M_e / M_c(<r_ta) and M_e = ∫_{r<r_edge} max(ρ_ph − ρ_c, 0) dV.
- **F_dd** = F_nodd + PROP. It holds exactly M_ta inside r_ta.
- **SHELL (variant):** −q_sh ρ_c on r_edge < r < r_ta. It is **infeasible for 75–87% of lens groups** (q_sh > 1, overdraw), and the edge reaches r_ta in 2–4% of groups.

**Typical lenses (z = 0.3):**

| log M* | r_ta | r_edge (can / alt) | f_ret | q (can / alt) | PROP at R = 0.1/0.3/0.6/1/2 Mpc (can) |
|---|---|---|---|---|---|
| 10.5 | 0.91 Mpc | 0.40 / 0.36 | 0.10 | 0.34 / 0.36 | −4.6 / −1.24 / −0.46 / −0.22 / −0.05 Msun/pc² |
| 10.75 | 1.21 Mpc | 0.70 / 0.63 | 0.08 | 0.30 / 0.31 | −6.7 / −2.0 / −0.80 / −0.38 / −0.11 |
| 11.0 | 2.03 Mpc | = r_ta | 0.03 | 0.14 / 0.18 | −6.8 / −2.7 / −1.2 / −0.61 / −0.23 |

**Stacked 15-bin PROP** (bins at R = 2.17 … 0.046 Mpc), in Msun/pc²:
- canonical: [−0.060, −0.116, −0.203, −0.322, −0.485, −0.734, −1.095, −1.602, −2.291, −3.197, −4.339, −5.710, −7.282, −8.984, −10.713]
- alt: [−0.063, −0.124, −0.218, −0.345, −0.521, −0.788, −1.174, −1.717, −2.455, −3.423, −4.645, −6.110, −7.787, −9.602, −11.447]

**Amplitude and range:**
- **Amplitude:** −18 to −23% of F_nodd + 2h in every bin (canonical) and −19 to −24% (alt).
- **Radial range:** the whole catchment, 0 < r < r_ta. For the stack that is all 15 bins (0.05–2.2 Mpc). For the SHELL variant it is r_edge–r_ta (about 0.4–1.2 Mpc), with −0.06 to −0.2 Msun/pc².

**Stated before the test.** PROP is close to a uniform ~20% rescaling of the cold halo. It is therefore **degenerate with the SHMR halo-mass normalisation**: with a free halo amplitude it cannot be seen at all. On KiDS alone this is an amplitude test, conditional on Moster+13 masses.

**Frozen two-halo term** (never freed in the verdict). The lensing by everything outside each lens's own r_ta ball, stacked in the S0 control (512³, both seeds, 3 projections) around peaks of matching M_ta (log M_ta 12.0–13.8 Msun/h):
- Isolation: no peak with M ≥ 0.5 M within 3 Mpc/h (iso05; the available cut closest to the B21 criterion).
- Mapped to the lens by R_com = R(1+z)h and ΔΣ × h(1+z)² D(z)².
- Below 2 cells (0.78 Mpc/h comoving), an R² taper.
- Expressed in CFG377's R^-0.8 template, this term is **A_equiv = 0.07**. The free fits of CFG413/486 needed 0.95–1.57.

## Step 3 test (cfg495_test.py), data = CFG377 primary stack
181,477 lenses, 15 g_bar bins, 50-patch jackknife, Hartlap 0.6735.

**Decision, per footing.** Δχ² = χ²(F_dd) − χ²(F_nodd), with the frozen two-halo term:
- **DETECTED:** Δχ² ≤ −4 on both footings (the data prefer the drawdown by ≥ 2σ).
- **EXCLUDED:** Δχ² ≥ +4 on both footings (the data disfavour the predicted drawdown by ≥ 2σ).
- **Otherwise NOT DIAGNOSTIC.** In that case the forecast is reported: λ, σ_A, and the data needed.

**Declared labels.** These are attached to the verdict and do not replace it.
1. **NOT CLEAN:** PILEUP (F_nodd − PROP, the opposite sign) beats F_nodd by Δχ² ≥ 4 on either footing. That would mean the data want more mass, not a drawdown.
2. **NOT ROBUST:** the per-footing verdict flips in any of these rows:
   - two-halo variants: iso1, all, D(z)¹, D(z)⁰, none;
   - halo mass M200 × 10^±0.2;
   - the f30 strict-isolation subset.
3. **MODEL-INADEQUATE:** the best frozen model (LCDM, F_nodd, F_dd) has p(χ², 15) < 0.001. A drawdown verdict on a misfitting baseline is not a measurement.

**Reported only:**
- the amplitude fit A_prop ± σ (prediction A = 1; mesh-limited A_sim ≈ 0.13–0.16);
- the three-way χ² (LCDM vs F_nodd vs F_dd);
- the SHELL variant;
- the 9 trusted bins (R ≤ 0.445 Mpc);
- a free R^-0.8 two-halo amplitude (CFG413's floor).

## MUTATE / controls
- **Opposite sign.** The pile-up must not be preferred (label 1).
- **Shuffled positions, simulation.** The drawdown stack at random centres must fall below 10% of the halo-centred amplitude (0.3–1 r_ta) in every mass bin (cfg495_sim_analysis.py, CFG495_MUTATE=1).
- **Shuffled positions, KiDS.**
  - Re-stack at lens positions displaced 1–2° (cfg495_stage_random.py, the CFG110 estimator verbatim). Repeat with the cross-shear stack (CFG116 WX).
  - In both, fit the drawdown alone. A must be consistent with zero (|A/σ| < 2); otherwise the label is SYSTEMATIC.

## Caveats (stated before the test)
- The two-halo term and halo mass are frozen from a 0.39 Mpc/h-mesh S0 control and a literature SHMR. CFG413/486 showed the outer KiDS bins carry a large excess that a free template absorbs.
- The simulation is at z = 0; the lenses are at z ≈ 0.3.
- The drawdown is bookkeeping in the engine (a source term), not moved cold fluid.
- f_ret uses the LCDM-equivalent M_ta.
- Nothing here derives κ, f_b or ρ_Λ. Nothing here says the data favour the framework.
