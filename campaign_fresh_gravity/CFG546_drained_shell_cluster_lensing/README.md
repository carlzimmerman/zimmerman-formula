# CFG546: the drained shell around settled halos in stacked lensing. The R5 engine predicts a strong shell; no on-disk dataset can test it; the best cluster stack (DES-Y3-like) reaches only Z ≈ 2 once splashback is marginalised. Verdict: NO CANDIDATE AT Z ≥ 3 (one MARGINAL); TEST NOT RUN

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (baf7e3dd4), before any script, stack or ΔΣ value.
- **Scripts:** `cfg546_predict.py` (Step P, templates), `cfg546_lib.py` (DK14, projection, constructed covariances, Fisher), `cfg546_forecast.py` (Step F), `cfg546_k3.py` (K3, reported).
- **Settings:** κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10, never pooled. Cold energy's MASS is still required; no particle species. Not "theory closed". Nothing here says the data favour the framework.
- **No downloads.** Data read: the CFG526/530 512³ and 256³ gravitating-density grids (R5 engine and matched S0), the committed CFG495 JSON, and the DESI DR1 LRG joint covariance plus r_p bin edges. **No DESI ΔΣ value was read** (the test was not adequate, so Step T never ran).

## Inventory (task 1)
- **On disk, reaching 1–3 r_ta:** only the DESI DR1 galaxy–galaxy lensing release (Heydenreich+25; Zenodo 22914838; `_external_data/desi_dr1_lensing/`, 46 MB). It holds BGS and LRG ΔΣ against KiDS-1000, DES-Y3, HSC-Y1/Y3 and SDSS in 15 bins from 0.08 to 80 h⁻¹ Mpc, with joint analytic covariances. These are galaxy-selected lenses (group-scale hosts, ~10% satellites), not halo-centred clusters. The files are labelled "blindA"; the paper's blinding function is linear in ln R, so m₁ is left free.
- **On disk, not usable:** Sifón+18 MENeaCS (`_external_data/sifon2018`, 2.6 MB LaTeX source) is satellite lensing inside clusters (R ≲ 2 Mpc). KiDS-bright isolated-lens stacks (CFG377/495/504) are galaxy-scale. No stacked cluster or group ΔΣ reaching 3–10 Mpc exists on disk.
- **Published candidates (not on disk; sizes (U), to check before any download):**

| ID | dataset | profile product | covariance | approx. size (U) |
|---|---|---|---|---|
| D2 | DES-Y3 redMaPPer stacked ΔΣ (DES Y3 cluster lensing / cosmology papers) | per λ–z bin ΔΣ to ~30 Mpc | jackknife / analytic, released with the cosmology chains if public | a few MB of tables; the full Y3 shear catalogue is ~100 GB class |
| D1 | DES-Y1 redMaPPer (McClintock+19; Chang+18 splashback) | ΔΣ in 12 λ–z bins, 0.03–30 Mpc | yes (semi-analytic + jackknife) | a few MB |
| D6 | eRASS1 clusters × DES/KiDS/HSC (Grandis+24) | shear profiles 0.5–3.2 Mpc | yes | MB |
| D4 | HSC × CAMIRA / SDSS redMaPPer (Murata+19 class) | ΔΣ 0.1–15 Mpc | yes | MB |
| D8 | ACT DR5 × DES-Y3 / HSC (Shin+21 class splashback) | mostly galaxy-density profiles; ΔΣ to ~10 Mpc | partial | MB |
| D7 | SPT × DES-Y3 (Bocquet+24) | 0.5–3.2 Mpc | yes | MB |
| D3 | SDSS redMaPPer × SDSS shear (Simet+17) | ΔΣ to ~30 Mpc | yes | MB |
| D5 | KiDS × GAMA groups (Viola+15; Dvornik+17) | to ~2 Mpc | yes | MB |
| — | Euclid Q1 | no tabulated stacked cluster profile known (U) | — | — |

## Step P: what the R5 engine predicts (`cfg546_predict.out`)
This is the first measurement beyond r_ta of THEORY_v1 rule R5 (draw only from the shell between the census edge and r_ta). Stacks are around S0 centres. rel(x) = ⟨ρ_g,F − ρ_g,S0⟩ / ⟨ρ_g,S0 − 1⟩, with x = r/r_ta.

| run | bin | N | median log M_ta | median r_ta (cells) | inner excess E (0.2–1 r_ta) | depletion depth D (1–3 r_ta) | sign change |
|---|---|---|---|---|---|---|---|
| 512³ canonical | clusters | 295 | 14.44 | 4.00 Mpc/h (10.2) | **+0.37** | **0.309 ± 0.027** | x = 0.85 |
| 512³ canonical | groups | 3282 | 13.51 | 1.95 (5.0) | −0.03 | 0.153 ± 0.007 | none (deficit throughout) |
| 256³ canonical | clusters | 242 | 14.47 | 4.10 (5.2) | +0.16 | 0.148 ± 0.018 | x = 0.55 |
| 256³ alt | clusters | 242 | 14.47 | 4.10 (5.2) | +0.21 | 0.171 ± 0.017 | x = 0.65 |
| 256³ both | groups | 3725 | 13.37 | 1.76 (2.2) | — | — | UNRESOLVED, does not count |

- **Clusters, 512³:** the effective density is +32% above S0 at 0.45 r_ta. It crosses zero at 0.85 r_ta, sits at −29% at 1.05–1.35 r_ta and −14% at 1.65 r_ta, and is back near zero by 2.2 r_ta. **So R5 predicts a real drained shell just outside r_ta, about 30% deep.**
- **In projection the shell hides.** The cluster ΔΣ ratio stays positive: +22 to +28% at 0.45–0.75 R/r_ta, falling to 0 near 2 R/r_ta. Lensing sees the inner excess plus a steep fall-off, not a ΔΣ deficit (as CFG495 found).
- **Groups:** a deficit of −10 to −17% from 0.45 to 1.35 r_ta, decaying to zero by about 3 r_ta.
- **Not converged.** The 512³ cluster amplitude is 2.03× the 256³ one (s_res). The alt 512³ template is the 256³ alt template × 2.03 (the frozen construction). No alt group template counts, because the 256³ groups are unresolved.
- **Controls:**
  - K1 PASS: mass conserved to 2e-9; F–S0 correlation at 8 Mpc/h 0.988–0.994.
  - K2 PASS: 99.5–99.6% of centres.
  - K4 PASS: projection vs analytic NFW, 0.13%.
  - **MUTATE-SIM FAIL, by the frozen statistic.** The mean |rel| over 1–3 r_ta at random centres is 0.116–0.119 of the halo-centred value at 512³ (gate 0.10), and 0.20–0.36 at 256³. Post-freeze diagnosis (reported): the random-centre rel is consistent with zero bin by bin (χ² 14–29 for 20 bins). The signed means are +0.005 / +0.012 against −0.071 / −0.085 halo-centred. The failure is the noise floor of a mean-of-absolute-values statistic, not a signal at random positions. The frozen FAIL stands.
  - **K3 (reported) FAIL at 512³, PASS at 256³.** Projecting the 3D template on the stacked S0 profile does not reproduce the simulation's own ΔΣ ratio at 512³: clusters +0.14 vs +0.22 at 0.45 R/r_ta; groups −0.07 vs −0.02. So the 3D-template forecast carries a template-shape systematic of this size.

## Drained shell vs splashback (the key degeneracy)
- **Where each sits.** Splashback (the steepest slope of the DK14 fiducial) sits at **r_sp ≈ 1.1–1.3 r_200m ≈ 0.28–0.35 r_ta** for every dataset. The R5 shell sits at 0.85–2 r_ta, a factor of about 3–5 further out. In principle the radial separation is the lever.
- **In ΔΣ the lever is weak.** The projected signature (an excess inside r_ta, then a steep return) looks to DK14 like a **larger truncation radius plus a shallower outer slope**.
  - corr(A, ln r_t) is −0.76 to −0.85 for the cluster datasets.
  - Freeing splashback (r_t, β, γ) raises σ_A by ×1.7–2.4.
  - For DES-Y3-like errors the unmarginalised template is Z ≈ 12. Marginalising the full DK14 baseline (r_t, β, γ, b_e, s_e, ρ_s, r_s, α, m₀, m₁) leaves Z ≈ 2.
- **Apparent splashback shift (reported only):** absorbed into a ΛCDM DK14 fit, the R5 shell would push the inferred r_sp **outward by +26 to +35%** for the cluster stacks. The linear bias is unreliable where it exceeds the fitted range (the D6 published-range rows give a meaningless −89%). Comparing with published lensing splashback radii would be a separate, owner-approved lane. No published value was used here.

## Step F: the forecast (`cfg546_forecast.out`; Z = 1/σ_A, splashback marginalised)
Z on the canonical / alt footings, primary R5 template. Constructed covariances use (U) parameters.

| dataset | best range | Z canonical | Z alt | Z, 256³ template | Z, CFG495 template | splashback cost |
|---|---|---|---|---|---|---|
| **D2 DES-Y3 redMaPPer (16,000)** | 0.3–29 h⁻¹ Mpc | **2.06** | **2.19** | 0.96 | 1.17 | ×1.74 |
| D1 DES-Y1 redMaPPer (6,500) | 0.3–28 | 1.38 | 1.51 | 0.66 | 0.79 | ×1.81 |
| D6 eRASS1 (2,200), extended | 0.3–30 | 1.14 | 1.34 | 0.59 | 0.68 | ×1.86 |
| D4 HSC-Y3 (1,800), extended | 0.3–30 | 0.90 | 1.05 | 0.47 | 0.55 | ×1.93 |
| D8 ACT (1,000), extended | 0.3–30 | 0.76 | 0.71 | 0.31 | 0.39 | ×1.96 |
| D7 SPT (700), extended | 0.3–30 | 0.73 | 0.57 | 0.25 | 0.34 | ×1.79 |
| D3 SDSS (5,500) | 0.3–25 | 0.40 | 0.52 | 0.23 | 0.25 | ×2.39 |
| DESI DR1 LRG1 (on disk) | 0.5–80 | 0.20 | n/a (alt group template unresolved) | — | 0.05 | ×1.05 |
| DESI DR1 LRG2 (on disk) | 0.5–80 | 0.18 | n/a | — | 0.04 | ×1.06 |
| D5 KiDS×GAMA groups | 0.3–30 | 0.12 | n/a | — | 0.12 | ×1.04 |

- **D2 variants (canonical):**
  - r_ta +0.05 dex: 2.23 (extended range); −0.05 dex: 2.08;
  - covariance × 1.3: **1.81**;
  - LSS × 2: **1.91**.
  - So D2 falls below 2 under either shared-systematic inflation.
- **Published ranges cripple the SZ / X-ray stacks.** At ≤ 3.4 Mpc, D6 gives Z 0.61 and D7 0.10. They only reach r_ta ≈ 5 Mpc/h if re-measured from the shear catalogues.
- **DESI is not adequate.** Z 0.16 (primary range) on canonical. The group template's near-uniform deficit is absorbed by s_e and b_e: corr(A, s_e) = +0.92. The alt group template does not exist at a resolved scale. By the frozen rule the DESI data vector was never fitted.
- **MUTATE-FORECAST** (`cfg546_forecast_MUTATE.out`; 300 noise realisations, full nonlinear fit with priors):
  - **D2-extended canonical: PASS both.**
    - A = 0 injected: mean Â +0.019 (σ_A Fisher 0.486; +0.04σ); 2.3% beyond 2σ.
    - A = 1 injected: mean Â 0.954 (−0.10σ); scatter 0.434 against Fisher 0.486 (ratio 0.89).
    - The cluster forecast statistic recovers both null and signal.
  - **DESI LRG1 canonical: FAIL both.**
    - A = 0: mean Â −2.12; 0.7% beyond 2σ, below the 2% floor.
    - A = 1: mean Â −0.87; scatter 3.4 against Fisher 6.2 (ratio 0.55).
    - At σ_A ≈ 6 the priors and nonlinearity dominate, so the Fisher number is not a valid error there. It cannot change the adequacy decision: DESI is non-diagnostic either way (Z ≈ 0.2 by Fisher, ≈ 0.3 by the realisation scatter).

## Verdict (frozen rule)
- **Task 3: TEST NOT RUN.** The one on-disk dataset (DESI DR1 LRG) is not adequate: Z ≈ 0.2 < 3, and there is no resolved alt group template.
- **Cluster downloads: no candidate reaches Z ≥ 3 on both footings.**
  - One is **MARGINAL**: D2, DES-Y3 redMaPPer stacked ΔΣ, Z 2.06 / 2.19.
  - The NOT POSSIBLE threshold (no candidate ≥ 2) is not met, and |corr(A, ln r_t)| < 0.9 for the best candidates.
  - The frozen rule therefore gives **neither TEST NEEDS DOWNLOAD (needs Z ≥ 3) nor NOT POSSIBLE**. The honest reading: at current stack precision, with splashback and the outer slope marginalised, the drained shell is at the 2σ edge for the largest optical cluster sample and below it for everything else.
  - The marginal Z rests on the 512³ template. With the 256³ template every candidate falls below 1. The RESOLUTION-CONDITIONAL label (defined for Z ≥ 3) does not trigger, but the same caution applies.
- **Download list, if the owner wants the marginal test anyway:**
  1. DES-Y3 redMaPPer stacked ΔΣ tables with covariance (MB-scale tables; forecast Z ≈ 2.1, falls to 1.8–1.9 under covariance or LSS inflation). It must reach ≥ 15 h⁻¹ Mpc comoving, about 3 r_ta.
  2. DES-Y1 McClintock+19 ΔΣ tables (MB-scale; Z ≈ 1.4–1.5) as a cross-check only.
  Neither is decisive on its own. The real lever is the **apparent splashback shift**: the R5 shell predicts lensing r_sp pushed outward by about +30% if absorbed by a ΛCDM fit. That is a cheap check against published lensing splashback radii, to be frozen as its own lane.
- **What a result would mean:** a 2σ preference for A > 0 in D2 would be a hint only, given the template systematic (K3) and the non-converged amplitude. A 2σ exclusion of A = 1 would exclude the 512³ R5 amplitude, but not the 256³ one.

## Caveats
- The templates are z = 0 products of 0.39 / 0.78 Mpc/h meshes. The amplitude doubles from 256³ to 512³; no continuum value exists.
- All non-disk survey parameters are recalled (U). The constructed covariances (shape noise + Limber LSS from camb halofit + 25% intrinsic halo-to-halo scatter) ignore miscentring, boost, photo-z spread in Σ_crit and cluster–cluster correlation (that last one is bounded by the LSS × 2 variant). Each forecast is provisional until the paper's tabulated errors are read.
- The DK14 fiducial (diemer19 c, Gao α, DK14 r_t, β 4, γ 6, b_e 1, s_e 1.5) is ΛCDM standard practice, not fitted to any data here.
- κ is fitted and the cold energy's mass is still required. A drained shell, if ever seen, would not derive either.

## Run
```
nice -n 10 python3 cfg546_predict.py                      # Step P (~1 min) -> cfg546_predict.out / _results.json
CFG546_MUTATE=1 nice -n 10 python3 cfg546_predict.py      # shuffled centres -> *_MUTATE.*
nice -n 10 python3 cfg546_k3.py                           # K3 (reported)
nice -n 10 python3 cfg546_forecast.py                     # Step F (~15 min; camb halofit)
CFG546_MUTATE=1 nice -n 10 python3 cfg546_forecast.py     # MUTATE-FORECAST (300 realisations x 2 x 2)
```
