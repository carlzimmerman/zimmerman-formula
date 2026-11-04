# LAM11_imf_edge_diagnostic: NOT DIAGNOSED, as frozen, because the MUTATE check fails. The runs themselves point to the red end outside the IMF windows: cutting the fit at 7400 Å removes LAM10's pile-up, while masking Na I, CaT or TiO does not

| step | commit |
|---|---|
| Criteria, frozen first and committed alone | `c6f59aea4c` |
| Scripts and frozen draws, before any fit | `5807e8ec53` |

κ = ½ FITTED; not theory closed. This lane grades no law; it diagnoses a fit. No download. The cold sector stays retired.
Nothing here says the data favour the framework.

## The runs (100 real sums; LAM10's single-slope profile, variant A, plus one change)
| run | edge fraction (Γb 0.3) | median Γb | Spearman(Γb, log σ) [95 %] | removes the pile-up? | median α_KU2 |
|---|---|---|---|---|---|
| M0 (none) | 0.57 | 0.30 | -0.350 [-0.524, -0.142] | no | 4.73 |
| M_Na (8143-8244 masked) | 0.58 | 0.30 | -0.355 [-0.528, -0.151] | no | 4.73 |
| M_CaT (8474-8792) | 0.52 | 0.30 | -0.370 [-0.537, -0.168] | no | 4.62 |
| M_TiO (5816-6455) | **0.79** | 0.30 | -0.255 [-0.436, -0.059] | no | 4.91 |
| M_IMF (all three) | **0.77** | 0.30 | -0.299 [-0.472, -0.096] | no | 4.92 |
| M_blue (window ends at 7400) | **0.01** | **1.33** | -0.193 [-0.372, **+0.001**] | **yes** | **1.16** |

**M0's χ² gain of Γb 0.3 over Γb 1.3, by region** (median per galaxy, with the share of the summed +19,327):

| region | median gain | share |
|---|---|---|
| blue-other | +47.3 | **+0.49** |
| red-other (7400-8900, outside Na and CaT) | +14.1 | **+0.36** |
| CaT | +16.0 | +0.17 |
| Na | -2.8 | -0.01 |
| TiO | -1.4 | -0.01 |

## Checks
- **K0 PASSES.** M0 reproduces LAM10's Γb_best and grid index for all 100 galaxies exactly (largest difference 0).
- **K1 PASSES.** On 100 synthetics no mask creates edge hits: the edge fraction is 0.00 in all six runs. The median
  Γb_best - Γb_in is between -0.003 and +0.003, or +0.030 for M_blue. The median log α bias is +0.001 to +0.006. α_in was
  reproduced exactly.
- **MUTATE FAILS.** With Γb_best shuffled across galaxies, five runs' Spearman intervals include 0. M_IMF's comes out
  +0.185 [+0.002, +0.361], which just excludes 0.
  - Six independent 95 % intervals fail one such check about one time in four by chance alone. So the frozen line was too
    strict for six runs.
  - It is frozen, so the label is **NOT DIAGNOSED**. The shuffle is not re-run with another seed.

## Reading (not the label)
- Without the MUTATE failure, the frozen lines would give **DRIVEN BY THE RED END, OUTSIDE THE IMF WINDOWS**: M_blue removes
  the pile-up and M_IMF does not. Even then M_blue clears the σ line by only +0.001.
- **The IMF lines are not the cause.**
  - Na I and TiO both fit better at Γb 1.3 than at 0.3: their gains are negative.
  - Masking TiO or all three regions makes the pile-up worse (0.79 and 0.77). The lines that carry the IMF signal were
    holding the fits back from the top-light edge.
- **The red end outside those windows is what tips the fits.** Red-other carries 36 % of the gain, and CaT carries 17 %.
  - Suspects in the data: residuals of the 7600 Å oxygen band and the 8100-8400 Å water band, and red flux calibration.
  - Suspects in the models: the E-MILES stretch from 7410 to 8350 Å, which comes from a different stellar library. Its
    telluric residuals were not tested here.
  - Blue-other carries 49 % of the gain in M0, but cutting the red end alone leaves a blue-only fit at Γb 1.33. The blue
    prefers Γb 0.3 only while the red end is in the fit, through the shared polynomial and templates.
- **A blue-only fit (3900-7400 Å) gives Kroupa-like IMFs** (median α_KU2 1.16), with a weak σ trend (-0.19).
  - Most IMF information is gone below 7400 Å, apart from TiO.
  - Its K1 numbers are fine (+0.03 in Γb).
  - Using it would need its own frozen criteria.

## Template advice
**None is advised.**
- The frozen label is NOT DIAGNOSED.
- The reading points away from what α- or Na-enhanced templates would fix:
  - masking Na I changes nothing, so Na-enhanced E-MILES is not indicated;
  - the α-enhanced bimodal models on the MILES share are optical only (3540-7410 Å), so they can't touch a red-end driver.
- For the record, the candidates on the share (no download) are:
  - α-enhanced, optical: `MILES/MILES_BASTI_BI_Ep0.00.tar.gz` (131,221,336 B), `MILES/MILES_BASTI_BI_Ep0.40.tar.gz`
    (130,836,265 B) and `Photometric_predictions/out_mass_BI_BASTI_alpha` (970,536 B).
  - Na-enhanced, Padova00 only: `Other_predictions/E-MILES_NaFe_Enhanced/Ebi_NaFep03.tar.gz` (635,077,266 B) up to
    `Ebi_NaFep12.tar.gz` (634,895,361 B).

## Run notes
- **Processes.** Two single-thread processes ran from 17:37 to 18:24 with `nice -n 10`. All 1200 profiles succeeded (600 real,
  600 synthetic).
- **Memory, both measures.**
  - Physical footprint stayed near 0.17 GB per process (peak 0.90-0.93 GB, while loading).
  - RSS grew from about 0.6 to 1.5-1.8 GB per process, despite returning freed memory after every profile. The largest
    total RSS seen was 4.7 GB.
- **Not blind:** every LAM10 number was known before freezing.

## Files
`FROZEN_CRITERIA.md`, `lam11_sample.json`, `lam11_core.py`, `lam11_run.py`, `lam11.out` / `.json` and `lam11_MUTATE.out` /
`.json`. The per-run lines are in `lam11_runs.json`.

κ = ½ FITTED; not theory closed.
