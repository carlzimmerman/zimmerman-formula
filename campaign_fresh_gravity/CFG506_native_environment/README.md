# CFG506: a framework-native lensing ruler from the zero-knob simulations. NATIVE RULER INVALID by its own photometric check (both variants, all footings); no KiDS model verdict. Gravity part of the ruler difference is small: the zero-knob environment is 3-12% weaker than the S0 control's

Criteria: `FROZEN_CRITERIA.md`, committed alone before any script (27a6c64ee). Local compute on our own snapshots only; no downloads. nice 15, at most 4 threads, one 512^3 load at a time.
- kappa = 1/2 is FITTED. Footings 9.3603e-11 and 1.1312e-10 scored separately, never pooled.
- "Cold energy" = the cold clumping component. Its mass is still required; no particle species is added.
- Nothing here says the data favour the framework. Not "theory closed".

## What was built (owner's point, 10-08)
The KiDS environment term in CFG502/503/504 is built from LCDM ingredients and validated by asking LCDM to fit. This lane builds it instead from the zero-knob rule's own boxes (CFG424 engine, RC = 0; 512^3 FLAT canonical seeds 359 + 360, FLAT alt 359, DE canonical 359), and validates it with a check that assumes no gravity model.
- **Lensing mass** = the engine's own Poisson source: particles (baryons + cold energy) + S = e - comp (phantom excess inside the edge balls minus the per-catchment draw). Recomputed read-only with the engine's functions. K1: q_max reproduced to 1e-7 on every TA box. K2: S sums to zero (|sum S| / sum e ~ 2e-5).
- **Halos**: CFG504's finder, copied. C10: matches CFG504's on-disk S0 catalogue exactly (18,964 of 18,983 matched, median |d log M| = 0).
- **Galaxies**: each box's own halos abundance-matched to the GAMA SMF (Baldry+12, (U)), satellites by CFG502's occupation (M_1 = 17 M_min, host M_ta), placed on host particles. No LCDM HMF, bias, NFW or SHMR enters the ruler.
- **Selection**: photo-z isolation emulated per axis and z node with the measured close-pair kernel; leaked satellites enter as photo-z allows.
- **E_native** = DeltaSigma of the lensing field around each isolated box lens, with each central's own r_ta sphere removed (record convention). 27-subvolume jackknife.

## Bottom line
1. **The native ruler fails its frozen validation.** The photometric companion count (lenses log M* >= 10.44, 77% of the lensing weight) is measured 0.205 per lens. The ruler predicts:

   | ruler | variant F (frozen) | variant P (departure D1) |
   |---|---|---|
   | canonical | 0.313 (ratio **0.653**) | 0.499 (ratio **0.410**) |
   | alt | 0.311 (0.660) | 0.483 (0.425) |
   | DE canonical | 0.313 (0.657) | 0.491 (0.418) |
   | S0 (same pipeline) | 0.323 (0.634) | 0.536 (0.382) |

   Every ratio is outside [0.67, 1.5], so every ruler is **INVALID**. By the frozen rule there is no model verdict and no answer to "does the framework fit with its own ruler". The all-lens ratio, reported only, is 0.72-0.75 in variant F.
2. **The failure is in the galaxy-halo rule, not in gravity.** The S0 boxes fail the same way.
   - The boxes make too many leaked satellites: the stack-weighted fraction is 0.34 (F) / 0.43 (P), against CFG502/503's HOD value of 0.18.
   - The parent satellite fraction at log M* 10.5-10.6 is 0.66 in the box. Observed values are ~0.3, which is (U) recalled.
   - Cause: the joint abundance match to the GAMA SMF puts KiDS-mass centrals in lighter halos (log M_ta 12.0 at 10.5, against ~12.4 for the record's inverse Moster). N_sat = M / (17 M_min) is then about 3x larger per host.
   - This was verified as a model consequence, not a bug: the analytic parent fraction from the box HMF and the SMF is 0.43 above 10.5, the same as the drawn catalogue.
3. **How different are the two rulers?**
   - **Construction:** large. The native S0 ruler fails MUTATE S0 against CFG504's committed E (9/15 bins within tolerance, both variants).
     - Inner trusted bins: native E is 0.11-1.7 against CFG504's 0.85-2.4 Msun/pc^2. The box host term around satellites is PM-softened below ~0.4 Mpc/h, so this part is mesh-limited.
     - Outer bins (1-2.2 Mpc): F gives 0.12-1.3; P gives 1.2-2.2, against 0.86-1.0.
     - Native E carries an isolation-induced **negative** centrals term (-0.2 to -0.44 at 1-2.2 Mpc). It appears because isolated lenses sit in projected-underdense surroundings. The LCDM-native term does not model this.
   - **Gravity (TA vs S0, identical pipeline):** small.

     | | variant F | variant P |
     |---|---|---|
     | TA / S0 | 0.94-0.97 (0.88 at 2.2 Mpc) | 0.89-0.99 |
     | difference per bin | <= 0.21 sigma_data | <= 0.79 sigma_data |
     | difference vs box jackknife | 2-5 sigma | 2-5 sigma |

     The S share (phantom minus draw) is -0.01 (F) to -0.06 (P) Msun/pc^2 at 0.4-1 Mpc. That is the drawdown around hosts.
4. **The re-score, information only (ruler INVALID).** Native canonical ruler, variant F, 9 trusted bins:

   | model | canonical chi2 (p) | alt chi2 (p) | with CFG503 E (canonical) |
   |---|---|---|---|
   | LCDM | 13.05 (0.16) | 13.05 (0.16) | 7.60 |
   | F_dd (zero-knob engine-rule lens) | 21.67 (0.0100) | 23.10 (0.006) | 5.24 |
   | F_nodd (reported) | 12.79 (0.17) | 13.39 (0.15) | 9.56 |
   | law to r_ta | 120.4 | 90.7 | 60.7 |
   | V1 | 119.7 | 89.8 | 60.1 |
   | 5.85 r_M edge | 329.4 | 328.4 | 240.9 |

   - Variant P is similar: LCDM 12.05, F_dd 21.10 (p 0.012), edge 302.
   - Full 15 bins, variant F: LCDM 62.6, F_dd 56.3, edge 526.
   - **The native ruler does NOT rescue the framework's models. It makes F_dd worse on the trusted bins (5.2 -> 21.7)**, because the mesh-limited native E is smaller there. The LCDM-native ruler was the more favourable one for F_dd in the inner bins.
   - CFG504's committed stack-P chi2 (15 bins, its smooth window), for reference: LCDM 18.5, F_dd 13.7 / 14.2, edge 395 / 397.

## Departures and fixes (dated 2026-10-08, all before any KiDS re-score)
- **D1 (variant P), decided after seeing the box isolation pass fraction.**
  - The frozen neighbour threshold (the pool's 5th percentile mass) treats the flux-limited pool as complete. The box then vetoes ~5x too often: box pass fraction 0.04 vs KiDS 0.28 at z 0.25.
  - Variant P sets a completeness step m_c(z) = 9.99 / 10.42 / 10.75 / 10.97 at z 0.15-0.45. The step is chosen so that the SMF density reproduces the MEASURED chance count of qualifying neighbours (4-6 Mpc annulus pairs; photometry only).
  - It then reproduces KiDS's isolation pass fraction with no further input: 0.23 / 0.53 / 0.78 vs 0.28 / 0.55 / 0.78 at z 0.25 / 0.35 / 0.45. At z 0.15 it gives 0.07 vs 0.19.
  - Both variants are carried to the end. The frozen F gets the frozen verdict.
- **Fix, C3 failed in the first run (kept).** The bare Fourier disc filter rang by up to 7.7% at R >= 3 fine cells. The filter now carries a Gaussian taper (sigma = 1 fine cell; CIC deconvolved), and the own-sphere content gets the same smoothing exactly (Rice-CDF table). Lens centres are snapped to fine-grid nodes (<= 0.04 Mpc/h). After the fix C3 = 6e-4.
- **Fix, MUTATE SHUF failed in the first run (kept).** The box stores +DeltaSigma of the uniform sphere, and the first scoring used it as H with the wrong sign. With the hole H = -DeltaSigma, as the criteria define it, SHUF passes on every ruler. The box code is unchanged.
- **Implementation detail.** The abundance match needs n(> M) below the 150-particle completeness, for faint neighbours and satellites. There the box HMF is continued as a power law fitted on [M_c, 10 M_c] (slope 0.60 at 512^3). Lens bins are built only above completeness (log M* >= 10.44 / 10.42). For the 23% of stack-P weight below that, E is clamped at the lowest complete bin.

## Controls and MUTATE
- **Pass:**
  - C1: data = CFG377.
  - C2: this code with CFG503's E reproduces CFG503's 14 chi2 (max |d| 0.0000).
  - C3: 6e-4 (after the fix).
  - C4: measured companions = CFG502's 0.2537.
  - K1, K2 on all 12 TA boxes.
  - C10 (exact).
  - **MUTATE SHUF** (shuffled centres carry no environment): 15/15 bins on every ruler and variant. Mean |E_shuf - H| / |E_nat - H| = 0.005-0.019.
- **Fail (load-bearing, reported):** **MUTATE S0.** The S0-box ruler does not reproduce CFG504's LCDM-native term (9/15 bins, both variants). The native and LCDM-native constructions differ beyond the gravity model: the galaxy-halo rule, PM softening of host cores, and the isolation-induced centrals term.
- 256^3 boxes: m_lim,box = 11.02, so no lens bin and no ruler. They are used for diagnostics only.

## Zero-knob diagnostics pack (`cfg506_diag.*`, `figs/`)
- **D1, settled vs unsettled cold energy.** Settled mass fraction 0.162 (512^3), 0.109 (256^3). Edge balls fill 0.24% of the volume and catchments 3.7%. The phantom excess e equals the draw: 5.3% of the total mass (2.9% at 256^3). Slab maps: `figs/D1_*`.
- **D2, catchment draw q per host.**
  - 512^3: median q rises with host mass, from 0.02 (log M_ta 13-13.5) to 0.05 (13.5-14), 0.07 (14-14.5) and 0.20-0.23 (> 14.5).
  - 256^3: q falls with mass, 0.10-0.16 at 13-13.5 down to 0.04-0.06 at 14-14.5.
  - q_max 0.26-0.30 (256^3) -> 0.44-0.57 (512^3), set by the most massive hosts. Every box reproduces its run JSON.
- **D3, concentrations** (mesh-limited proxy from M(< r200m/2) / M200m). TA halos are less concentrated than S0 at matched seeds in every resolved bin: 1.40 vs 1.55, 1.52-1.68 vs 1.83-1.92, 1.07-1.22 vs 1.69. The absolute values are unphysical (the mesh sets them); only the ratio is meaningful.
- **D4, P_TA / P_S0** (z = 0, matched seeds).
  - 512^3 canonical: 1.007 +- 0.002 at k 0.2, 1.022 +- 0.008 at 0.5, 0.97 at 1, 0.84 at 2, 0.80 at 3 h/Mpc.
  - 256^3 (3 seeds): 1.019 at 0.5, 0.93 at 2.
  - max |P - 1| (k <= 1) 0.02-0.04.
  - **The zero-knob rule suppresses small-scale power by 16-20% at k 2-3 h/Mpc at 512^3**, consistent with the lower concentrations. sigma_8 ratio 1.002-1.005.
- **D5, halo mass function TA / S0:** 1.00 +- 0.02 from log M_ta 12 to 13.4. A weak deficit (0.84-0.98, within 1-1.5 sigma) above 14.
- **D6** (3D lensing-density profiles TA / S0): seed-noisy at 5-10%. For clusters (14-15.2), 0.83-0.90 at r 0.3 Mpc/h on seed 359 (0.98 on seed 360). S changes the ratio by <= 3%.

## What would make the native ruler valid (needs a new frozen lane; nothing tuned here)
- A satellite content checked against data: the observed satellite fraction or conditional SMF at log M* 10.5 for this selection. That needs the KiDS-bright x GAMA overlap or a GAMA group catalogue, so an owner go for the download. Or a galaxy-halo rule frozen in advance with a host-mass definition and normalisation tied to an observed satellite fraction.
- Higher resolution for the inner trusted bins. A 1024^3 box, or a zoom, to resolve host cores below 0.4 Mpc/h.
- Until then, the native construction says only this: the zero-knob gravity itself changes the environment term by <= 0.2-0.8 sigma_data per bin relative to S0. The large differences from CFG503/504 come from the galaxy-halo construction and the mesh, not from the gravity model.

## Run
```
./run_506.sh TA512_can359 TA512_can360 TA512_alt359 S0512_359 S0512_360 TA512_DEcan359 TA256_can359 ... S0256_361   # ~10 min per 512^3 box, sequential
nice -n 15 python3 cfg506_diag.py
nice -n 15 python3 cfg506_score.py ; CFG506_MUTATE=1 nice -n 15 python3 cfg506_score.py
```
Per-box tables (`cfg506_box_<KEY>.npz`) and logs live in `../../../_external_data/cfg506_work/` and are not committed. numpy prints spurious matmul RuntimeWarnings (the known Accelerate quirk); every table is finite.
