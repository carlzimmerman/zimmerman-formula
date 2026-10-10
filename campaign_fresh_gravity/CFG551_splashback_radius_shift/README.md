# CFG551: does the R5 drained shell push the inferred splashback radius outward? Verdict: NOT DIAGNOSTIC (data precision), FEW MEASUREMENTS. Two disclosures: the ΛCDM control on our own boxes FAILS (K-S0), and the CFG544 kinetic softening removes the predicted shift.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (b1b7c9e08), before any script, ratio or compiled number.
- **Scripts:**
  - `cfg551_ptemplate.py`: galaxy-tracer (particle) templates and K-DEP.
  - `cfg551_lib.py`: nonlinear noiseless DK14 fits and r_sp. It imports CFG546's lib unedited.
  - `cfg551_predict.py`: predictions, confrontation, verdict, K-S0, V7. Run it with `CFG551_MUTATE=1` for the MUTATE gates.
- **Compilation:** `cfg551_measurements.json`.
- **Settings:** κ = ½ is FITTED. The footings are 9.3603e-11 and 1.1312e-10 and are never pooled. The cold energy's mass is still required; no particle species is added. This is not "theory closed". Nothing here says the data favour the framework. Every number below is read from `cfg551_predict_results.json`, `cfg551_predict_MUTATE_results.json` or `cfg551_ptemplate_results.json`.
- **No downloads.** Particle fields were CIC-deposited from the committed z = 0 snapshots into `_external_data/cfg551_work/`, which is not committed.

## Task 1: compilation (all numbers PROVISIONAL)
- **Source:** arXiv abstracts and HTML, read through a web-fetch summariser (see the 10-02 rule). Check each number against the paper's own table before citing it.
- **Ratio rule:** R_obs = r_sp,data / r_sp,ΛCDM-sim, using the authors' own comparison. Errors are propagated and kept asymmetric.

| id | class | sample | R_obs | in the class combination? |
|---|---|---|---|---|
| Shin21_L | **L-SZX** | ACT DR5 × DES Y3 lensing, z 0.455, M500c 2.72e14 | 1.038 −0.255/+0.184 (2.20 vs MDPL2 2.12) | **yes (the only one)** |
| Contigiani19_L | L-SZX | CCCP, 27 X-ray clusters | no quoted ΛCDM r_sp | no |
| Mpetha25_L | L-SZX | UNIONS × M2C / SPIDERS | no ratio, mass or z | no |
| Chang18_L | L-OPT | DES Y1 redMaPPer lensing | 0.918 ± 0.147 (vs the subhalo 1.46) | yes |
| Shin19_SPT_G | G-SZX | SPT × DES Y1 | 1.097 −0.228/+0.257 | yes |
| Shin19_ACT_G | G-SZX | ACT × DES Y1 | 1.042 −0.269/+0.345 | overlaps the ACT sample: reported only |
| Shin21_G | G-SZX | ACT DR5 × DES Y3 | 0.976 −0.123/+0.057 | yes |
| Zurcher19_G | G-SZX | Planck PSZ2 × Pan-STARRS | 0.979 −0.159/+0.138 | yes |
| Rana23_G | G-SZX | eFEDS × HSC | 0.806 −0.148/+0.170 | yes |
| Chang18_G | G-OPT | DES Y1 redMaPPer galaxies | 0.774 ± 0.055 | yes |

- **Not usable** (no ratio, mass or z extracted): More+16 and Baxter+17 (SDSS redMaPPer; More+16's "20 ± 5%" is a second-hand quote), Shin+19 redMaPPer control (its simulation value came only from a figure description), Murata+20 (CAMIRA, agrees within 0.2–1.9σ), Giocoli+24 and Lesci+26 (AMICO), Adhikari+21, Bianconi+21.
- **Pattern:** optical redMaPPer galaxy densities sit about 20% low. The SZ/X-ray and lensing values are consistent with ΛCDM at the 10–25% error level.

## Task 2: predicted ratios (nonlinear DK14 fit, the way the papers do it, at each sample's M_200m and z)
- **Lensing (ρ_g templates):**
  - Primary: canonical **R_pred 1.17–1.28** and alt **1.17–1.19**.
  - With 256³ templates: **1.07–1.09**.
- **Galaxy density (new particle templates):**
  - In the tracer field the shell is much shallower than in ρ_g: −7% at 1.35 r_ta, against −28% in ρ_g.
  - Primary: canonical **R_pred 1.06–1.08** and alt **1.00–1.05**.
  - With 256³ templates: **1.00–1.02**.
- **CFG544 softening (V2):**
  - Stretching the template outward by s = 1.25 gives lensing R 1.03–1.17.
  - s = 1.55 gives **0.92–1.09** (lensing) and 0.95–1.00 (galaxies). **Kinetic support removes most or all of the shift.**
- **Other variants:**
  - σ_bin (0.02 or 0.10), constructed-covariance weights and CFG495 (1.03–1.05) leave the picture unchanged.
  - The 0.3–30 range raises the lensing R to 1.07–1.38.

## Confrontation (Z_i = (R_pred − R_obs) / σ)

| class | Z can / alt (primary) | Z can / alt (256³) | separation S (can / alt) | frozen verdict |
|---|---|---|---|---|
| **L-SZX (lane)** | **+1.11 / +0.81** | +0.22 / +0.30 | 1.32 / 1.02 | **NOT DIAGNOSTIC (data precision)**, FEW MEASUREMENTS |
| L-OPT | +2.43 / +1.76 | +1.03 / +1.15 | 1.87 / 1.20 | NOT DIAGNOSTIC (non-convergence on can; precision on alt); NOT ROBUST |
| G-SZX (4) | +2.14 / +1.10 | +0.99 / +0.88 | 1.48 / 0.44 | NOT DIAGNOSTIC (non-convergence on can; precision on alt) |
| G-OPT (1) | +5.65 / +4.96 | +4.56 / +4.57 | 1.54 / 0.85 | EXCLUDED by the rule, but **SELECTION-DOMINATED**; it does not set the verdict |

- **Lane verdict: NOT DIAGNOSTIC (data precision).** Only one lensing measurement on an SZ-selected sample exists with a quoted ΛCDM comparison (Shin+21). Its ±18–25% error cannot separate a +19–24% shift from ΛCDM at 2σ (S 1.0–1.3).
- **The leaning is worth stating, but it is not a result.**
  - Every clean class sits on the low side of the 512³ prediction (Z +0.8 to +2.4).
  - The G-SZX mean is 0.968 ± 0.049 against a predicted 1.01–1.08.
  - The tensions vanish with the 256³ templates (Z ≤ 1.2) and with the CFG544 softening.
- **Chang18_G (redMaPPer galaxies, 0.774) excludes even the 256³ and softened predictions (Z 3.3–5.8).** The same paper's lensing value and the SZ-selected galaxy values disagree with it, so the known optical-selection deficit dominates. It is not counted.

## Controls and MUTATE
- **K-DEP: PASS.** The CIC deposit reproduces the committed S0 ρ_p exactly (max diff 0) at 512³ and 256³.
- **MUTATE-0: PASS.** With zero shell, R = 1.0000.
- **MUTATE-SHUF: PASS.** Shuffled-centre template: R 1.001–1.003.
- **MUTATE-FULL: PASS.** CFG546's linear shifts are reproduced exactly (+26 to +35% for D1–D6, +14 to +26% for D7/D8).
  - The nonlinear fits at the same setups give **+24 to +36%** (σ_bin weights) and +19 to +34% (constructed covariance).
  - So CFG546's estimate holds up under a full fit.
- **K-S0: FAIL (gate).**
  - DK14 fitted to our own S0 512³ cluster stacks (CFG504 ξ_hm) gives r_sp **2.25–2.65×** the More+15 value, near the 3 r_200m search edge.
  - Diagnosis, from the stacked slope: at a mesh of 0.39 h⁻¹ Mpc the PM stacks show no splashback steepening. The log slope stays around −1.3 to −2.4 out to 2–3 Mpc and reaches only about −2.7 to −2.8 near r_ta. The mesh does not resolve the feature.
  - **Consequence:** our boxes cannot validate the r_sp pipeline. R_pred rests on the DK14 fiducial (the ΛCDM simulation calibration the papers use), with the template applied on top.
  - For the same reason, **the V7 sim route (ratio 3.40 for ρ_g, 1.22 for ρ_p) is not usable.** The K-ROUTE comparison (3.40 against the analytic 1.29) is uninformative.
  - Nothing was tuned after the failure.

## Caveats and disclosures (dated 2026-10-10)
- **Templates:**
  - The templates are z = 0 products of a PM run.
  - The 512³ shell amplitude is 2.03× the 256³ one (ρ_g); for particles s_res,p is 1.73. No continuum value exists.
  - The CFG544 stretch is a crude stand-in.
- **Masses:** samples quoted in M500c were converted to M200m with diemer19 c. Chang+18's mass is taken as h⁻¹ M_sun; its z is the range midpoint, and both are (U).
- **σ_pred uses only the template stacking error.** Variants V2–V6 reuse the primary σ_pred.
- **Not frozen, reported only:** `more15_constructed` in the JSON compares observed r_sp to More+15 at the converted mass. Its "Shin21_G" printout line actually belongs to the Adhikari21_G entry (r_sp 2.4, ratio 1.23); this is a print-order slip and no statistic uses it.
- **Process:** the summariser fetch saved two PDFs automatically (1811.06081, 2010.05920) to the session's tool-results folder. They were not decoded, and nothing here comes from them.
- **The decisive test needs a re-measurement:** lensing r_sp around SZ/X-ray-selected stacks (ACT DR5 / SPT / eRASS1 × DES Y3 / HSC) at ≲8% precision. Separately, a converged (finer than 512³) template, and a kinetic (CFG544 FIX-2-like) profile, since that alone can erase the shift.

## Run
```
OMP_NUM_THREADS=2 nice -n 10 python3 cfg551_ptemplate.py                 # ~3 min, ~4 GB peak
OMP_NUM_THREADS=2 nice -n 10 python3 cfg551_predict.py                   # ~25 min
CFG551_MUTATE=1 OMP_NUM_THREADS=2 nice -n 10 python3 cfg551_predict.py   # ~5 min (camb)
```
