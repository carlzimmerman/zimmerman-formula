# CFG502: the two-halo / environment term for the KiDS isolated-lens stack, built from first principles. MODEL STILL INADEQUATE by the frozen gate (LCDM chi2 45.9 / 15, p 5e-5); the clash verdict is therefore NOT DECIDED

Criteria: `FROZEN_CRITERIA.md`, committed alone before any script (cacadd50d). On-disk data only; no downloads. nice 15, at most 4 threads.
- kappa = 1/2 is FITTED. The footings 9.3603e-11 and 1.1312e-10 are scored separately and never pooled. a0 flat.
- "Cold energy" = the cold clumping component. Its mass is still required, and no particle species is added.
- Nothing here says the data favour the framework. Not "theory closed".

## Bottom line
1. **The record's "isolated" lenses are not isolated.** The isolation window is |Delta chi_phot| < 10 Mpc, but two galaxies at the same true redshift differ in photo-z distance by about 115 Mpc (Gaussian-equivalent sigma, measured here from close pairs; z < 0.3). So a satellite's own central vetoes it only **7%** of the time (p_10 = 0.068-0.071 at z < 0.3, measured).
   - With a standard halo model, about **17%** of the stack (stack-weighted) are satellites that leaked through. The parent sample has 25%, so isolation removes only about a third of them.
   - Photometry backs this up independently of lensing. Around the "isolated" lenses there are 0.25 more-massive companions per lens within 0.5 Mpc, above background. The model predicts 0.30 (ratio 0.85, inside the frozen [0.67, 1.5]).
2. **These leaked satellites are most of the "two-halo" excess.** Their host halos, seen off-centre, give 1.5-2.4 Msun/pc² at 0.3-0.8 Mpc and 0.36 at 2.2 Mpc. The centrals' true two-halo term outside r_ta is small (+0.15 at 2.2 Mpc), and **negative** (down to -0.23) at R ≈ r_ta because of the mean-density hole.
   - Adding this term takes LCDM from chi2 190.5 (centrals only, which is effectively CFG495's frozen PM term at 189.1) to **45.9**.
   - The MUTATE run with f_W = 0 confirms it: the outer-6-bin chi2 goes from 26.1 to 144.1.
3. **The frozen gate fails.** LCDM + E reaches chi2 45.92 / 15 (p = 5.5e-5), against the required p > 0.01. By the frozen rule the result is **MODEL STILL INADEQUATE**. No model verdict and no clash verdict are drawn. The table below is reported for information only.
4. **What is still missing** (post-hoc, in `cfg502_posthoc.*`):
   - **(a) The 1.0-1.4 Mpc transition.** The data sit +2.3 sigma and +4.0 sigma above LCDM + E there. The frozen term uses b xi_lin outside r_ta, which underestimates the nonlinear halo-matter correlation just outside turnaround.
   - **(b) The one-halo normalisation.** The inner 9 bins sit 1-2.6 sigma below LCDM (inverse-Moster masses with the +0.15 dex flux scale; satellites' own halos are not stripped in any model). The ALL stack shows the same pattern far more strongly (inner chi2 119 / 9).
   - Freeing a halo-mass shift of -0.2 dex together with one amplitude on E gives LCDM chi2 24.2 / 14 (s = 1.51). That is two knobs, and it is not a validation.

## The frozen re-score (stack P, 181,477 lenses, 15 bins, Hartlap 0.6735; the same E for every model; no free parameter). REPORTED ONLY: the gate failed

| model | canonical chi2 / 15 (p) | alt chi2 / 15 (p) | inner 9 / outer 6 (can) |
|---|---|---|---|
| (i) LCDM NFW (footing-free) | 45.92 (5.5e-5) | 45.92 (5.5e-5) | 22.3 / 26.1 |
| (ii) law to r_ta | 53.92 (2.7e-6) | 38.29 (8.2e-4) | 47.4 / 8.2 |
| (iii) 5.85 r_M edge (growth rule) | **429.12** | **431.47** | 236.7 / 171.3 |
| (iv) CFG487 V1 clock taper | 57.22 (7.5e-7) | 34.33 (3.1e-3) | 46.8 / 20.9 |
| (v) CFG495 drawdown F_dd | 23.28 (0.078) | 23.50 (0.074) | 4.8 / 25.2 |
| F_nodd (reported) | 51.42 | 60.82 | 30.6 / 20.3 |
| law to 0.5 r_ta (CFG413 best, reported) | 63.75 | 41.68 | 47.0 / 32.7 |

- Data are E(W = 10) and LCDM + E per bin; see `cfg502_score.out`.
- E at R = 2.17 / 1.04 / 0.44 / 0.11 Mpc is 0.50 / 0.86 / 2.25 / 1.70 Msun/pc². It is 15-36% of the signal at 0.19-0.44 Mpc (8% at 0.11 Mpc), so it reaches into the bins Brouwer+21 trusted.
- **F_dd's low chi2 is the halo-mass degeneracy CFG495 already named.** It is not a drawdown detection. The drawdown lowers the cold halo almost uniformly by 18-24%, which is what the inner bins ask of LCDM (compare the LCDM -0.2 dex row in the post-hoc).
- **The clash (edge vs lensing): NOT DECIDED by the frozen rule**, because the gate failed.
  - For information: on every reading tried, the edge is far worse than the best model on both footings. Frozen E: +405.8 / +408.0. One profiled amplitude on E: +89.1 / +84.9. Separate central and satellite amplitudes: +57.1 / +55.0. CFG413's free R^-0.8 on top of E: 47.4 / 53.0 against 16.3 / 17.8.
  - That is the CONFIRMED pattern, but it rests on a template that fails its own LCDM validation. Do not quote it as "confirmed".

## Nulls (frozen, reported)
- **N1, f30 (57,265 lenses, E at W = 30, where p_30 = 0.20-0.21):** LCDM chi2 34.11 / 15 (p 3.3e-3). This also fails, but is closer. The outer signal drops with stricter isolation, and E drops with it (0.35 at 2.2 Mpc, against 0.50 for W = 10), in the right direction. F_dd 8.5 / 8.4; law to r_ta 50.0 / 38.5; V1 44.0 / 29.8; edge 233.5 / 239.8.
- **N2, ALL (605,531 lenses, no isolation, re-stacked here with the CFG110 estimator verbatim):** LCDM + E(ALL) chi2 172.2 / 15. Inner 119.1, outer 34.9.
  - The outer bins are close: 1.92 against 2.24 at 1.96 Mpc, and 3.93 against 3.98 at 0.93 Mpc.
  - The inner bins are 15-25% above the data, which is the one-halo normalisation again.
  - The same +4.5 sigma pull at about 1.2 Mpc appears.

## PM cross-check (S0, 256^3, three seeds; reported)
- **Halo-model prediction (NFW holding M_ta + b_T10 xi_lin outside r_ta + hole) vs PM, for group peaks.** The median PM / model over [1.5 r_ta, 8 Mpc/h] is 0.78 (log M_ta 13.3-13.7; seeds 0.84 / 0.78 / 0.63) and 0.85 (13.7-14.3; 0.93 / 0.84 / 0.85). This is **inside the frozen [0.7, 1.3], so it passes**. The PM sits below the model, not above it. At 256^3 (0.78 Mpc/h mesh, 200 Mpc/h box) the PM misses both small-scale and box-scale power, so it cannot test the nonlinear boost that (a) above asks for.
- **Isolation emulation (group peaks; neighbour ratio 0.3 in M_ta).**
  - Photo-z isolation (sigma_chi = 54.5 Mpc/h) keeps 90-97% of the signal beyond r_ta. True-redshift isolation keeps 82-96%.
  - So for resolved group hosts neither cut removes much of the centrals' environment. CFG495's near-zero term is reproduced here by leaving the satellites out (f_W = 0 gives chi2 190.5 against CFG495's 189.1), not by the isolation cut.
  - KiDS-mass halos are not resolved, so this emulates the mechanism, not the sample.
- The 512^3 S0 was not run: KD-tree mass assignment on 134M particles is beyond this lane's light-CPU budget.

## Inputs measured here (photometry; the shear catalogue was not read for them)
| lens z | 0.10-0.15 | 0.15-0.20 | 0.20-0.25 | 0.25-0.30 | 0.30-0.35 | 0.35-0.40 | 0.40-0.45 |
|---|---|---|---|---|---|---|---|
| p_10 (veto prob., same-z pair) | 0.071 | 0.069 | 0.068 | 0.071 | 0.054 | 0.050 | 0.032 |
| p_30 | 0.210 | 0.209 | 0.204 | 0.211 | 0.169 | 0.166 | 0.131 |
| pair sigma (Gauss-equiv., Mpc) | 112 | 116 | 117 | 112 | 148 | 160 | 248 |
| companions: measured / predicted | 1.06 | 0.83 | 0.81 | 0.76 | 0.71 | 0.54 | 0.47 |

- Below z = 0.3, p_30 matches the Gaussian implied by p_10 to 0.01.
- The companion ratio falls with z because the prediction assumes every more-massive companion is in the r < 20 pool. That holds less well at high z. The stack-weighted ratio is 0.85.

## Controls and MUTATE
- **Pass:**
  - C1: the data equal CFG377's primary vector exactly.
  - C2a/b: the LCDM table equals cfg495_lenslib and CFG495's committed vector.
  - C2c: all five own profiles reproduce the record's free-template chi2 to 0.0000 (CFG413 x = 1 / 0.5, CFG487 edge, CFG498 V1, CFG495 F_dd).
  - C3: T2h via the shell projector equals the Hankel form, 6e-4.
  - C5: the isolation rebuild equals lr_lenses and f30 exactly.
  - C6: the ALL re-stack reproduces cfg110_perlens for the ISO lenses exactly.
- **C4 failed in the first env run, kept and fixed.** The offset kernel at zero offset differed from the centred NFW by 1.2%, against the 1% tolerance. The k-grid was 1e-4..1e3 with 40,000 points; it is now 1e-4..1e4 with 300,000. After the fix C4 = 4e-4. The model is unchanged; this was numerical precision.
- **MUTATE (`*_MUTATE.*`):**
  - M1, E = 0, reproduces CFG413's A = 0 law-to-r_ta chi2 (241.290 / 180.512) and CFG487's edge no-2h chi2 (1007.195 / 1013.152) exactly.
  - M2, f_W = 0, moves the LCDM outer-6 chi2 from 26.1 to 144.1. Both pass.
- numpy prints spurious matmul RuntimeWarnings (the Accelerate quirk seen in CFG77/100/377). Every table is finite, and C1-C6 confirm the numbers.

## What would close the gap (needs owner go where marked)
- **Local, no download:**
  - Replace b xi_lin outside r_ta with a nonlinear halo-matter correlation; CAMB with halofit is installed.
  - Add tidal stripping of the leaked satellites' own halos. Note that this changes the own profile of every model; it is not the shared E.
  - Both must be frozen anew before any re-score.
- **Needs owner go:**
  - The KiDS-bright x GAMA spectroscopic overlap, to measure the satellite fraction of this exact isolated sample directly.
  - The MICE mock with the KiDS-bright selection, which Brouwer+21 used to test isolation.
  - A 512^3 S0 halo catalogue with sub-structure, if the PM is to check the transition region.
- **Until a template passes its LCDM gate, no KiDS isolated-lens verdict beyond the inner ~0.1 Mpc should be read as decisive.** That covers verdicts from CFG352, 413, 486, 487, 495, 498, 501 and this lane. Even at 0.19-0.44 Mpc, 15-36% of the modelled signal is leaked-satellite environment.

## Run
```
nice -n 15 python3 -u cfg502_stage.py          # ~7 min; ISO rebuild, close pairs, companion counts, ALL re-stack -> _external_data/cfg502_work
nice -n 15 python3 cfg502_env.py               # ~1 min; E tables, p_W, C3/C4, companion check
nice -n 15 python3 -u cfg502_pm.py             # ~2 min; PM S0 cross-check
nice -n 15 python3 -u cfg502_score.py          # ~2 min; frozen re-score, nulls, gate, verdict
CFG502_MUTATE=1 nice -n 15 python3 -u cfg502_score.py
nice -n 15 python3 -u cfg502_posthoc.py        # POST-HOC diagnostics (not a verdict)
```
Large arrays (`cfg502_stage.npz`, `cfg502_env_table.npz`) live in `../../../_external_data/cfg502_work/` and are not committed.
