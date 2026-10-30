# GH3_tsz_cgm_extent

**Question.** GH2 found that on KiDS isolated lenses the lensing preference flips from the isolated law to route E if
the hot CGM extends beyond ≈ 1.8 R_vir. Zhang+24's X-ray stacks detect it only to R_vir. Does the gas around these
same lenses extend further?
- **Data:** ACT DR6.02 needlet-ILC Compton-y, fetched with the owner's OK as Dec strips (`_external_data/act_dr6_nilc/`).
- **Lenses:** the 88,861 KiDS isolated lenses in bins 3–4 (log M★ 10.6–11.0).
- **Method:** stack y in R/R_vir annuli, subtract randoms, and compare with beam-convolved predictions of Zhang's gas
  cut at k = 1, 1.8 and 3 R_vir (no free parameter).
- Criteria were frozen before any pixel was read (05e38c3ad3).

## Verdict

- **Standard map:** NEITHER FITS. The result is **CIB-SENSITIVE**.
- **CIB-deprojected map:** NOT DECIDED. It leans toward extended gas, landing exactly on the frozen threshold.

| y × 10⁸ per annulus (x = R/R_vir) | [0, 0.5) | [0.5, 1) | [1, 1.8) | [1.8, 3) | [3, 5) | null χ² (5) |
|---|---|---|---|---|---|---|
| **standard ILC**, 88,494 lenses | −2.5 ± 2.2 | 0.5 ± 1.8 | 3.8 ± 1.7 | 4.6 ± 1.3 | 1.4 ± 0.9 | 26.3 (p 8e-5) |
| **CIB-deprojected** | 0.6 ± 2.3 | 0.9 ± 2.0 | 1.2 ± 1.8 | 1.2 ± 1.6 | −1.3 ± 1.2 | 10.2 (p 0.07) |
| model, gas to 1 R_vir | 1.17 | 0.87 | 0.39 | 0.06 | 0.00 | |
| model, gas to 1.8 R_vir | 2.26 | 1.85 | 1.05 | 0.26 | 0.01 | |
| model, gas to 3 R_vir | 3.18 | 2.79 | 2.00 | 0.90 | 0.11 | |

| fit (χ², 5 annuli) | k = 1 | k = 1.8 | k = 3 | free amplitude A (k = 1 / 1.8 / 3) |
|---|---|---|---|---|
| standard | 30.7 | 34.7 | 33.8 | −4.1 ± 1.4 / −1.5 ± 0.7 / −0.4 ± 0.5 |
| **CIB-deprojected** | 8.7 (p 0.12) | 7.0 (p 0.22) | **4.7 (p 0.45)** | 2.7 ± 1.7 / 1.6 ± 0.8 / **1.23 ± 0.52** |

## What it shows

1. **The standard y stack is dominated by CIB.** A central deficit with a positive ring is the classic signature of
   the lens galaxies' own dust leaking into the ILC. Deprojecting the CIB removes the deficit, so the standard map
   cannot be used for this question.
2. **On the CIB-deprojected map, the data lean toward gas extending past R_vir, but do not decide.**
   - Gas to 3 R_vir at Zhang's own normalisation fits with no free parameter (p 0.45). Its free amplitude, 1.23 ± 0.52,
     is consistent with 1.
   - Gas stopping at R_vir would need 2.7 ± 1.7× Zhang's normalisation, and is also acceptable (p 0.12).
   - Δχ² = 4.0 between them sits exactly at the frozen threshold, so the verdict is NOT DECIDED.
3. **The lean is weaker than it looks.** The two-halo tSZ (correlated large-scale pressure), which is not modelled,
   also adds signal at 1–3 R_vir and would mimic extended gas.
4. **Subsets are too small to say anything.** z ≤ 0.25 (7,440 lenses) and G09 centrals (2,987) give null χ² p of 0.32
   and 0.50 on the standard map. The z ≤ 0.25 deprojected stack has a uniform −1.1 × 10⁻⁷ offset in every annulus, a
   large-scale random-subtraction mismatch on a small sample (deprojection amplifies large-scale noise).

**For the theory:**
- tSZ cannot yet settle whether the hot gas extends to the ~1.8 R_vir that route E needs to beat the law on KiDS
  lensing (GH2).
- The CIB-clean data are consistent with Zhang's gas continuing to ~3 R_vir, and do not exclude it stopping at R_vir.
- Getting more S/N means modelling the two-halo term and using a compensated-aperture or harmonic-space analysis on all
  ~180k isolated lenses: a methods upgrade, not a new fetch.
- κ = ½ FITTED; c_f EXTERNAL; cold dark energy is a gravitating field component, never a particle; not theory closed;
  nothing here says the data favour the framework.

## Checks (all PASS)

- **K1:** the β = 2/3 projection matches the closed form (−6.5e-5).
- **K2:** a synthetic beam source of known Y is recovered exactly (1.0000), and its annulus means match the beam at the
  same pixels (1.4e-2).
- **K3:** the pixel geometry matches astropy's WCS to 7e-11 px.
- **MUTATE:** random positions stacked as lenses give a null (χ² 4.4/5, p 0.50).
- Runtime < 1 min per run; peak RSS 0.66 GB; the strip is read in 400-row chunks.

## Files

- `FROZEN_CRITERIA.md`
- `gh3_tsz.py`
- `gh3_{map}_{sample}{,_MUTATE}.out` and `gh3_results_*.json`
- Data: `_external_data/act_dr6_nilc/` (FETCH_LOG.md, SHA256SUMS, strip_geometry.txt; ~1.66 GB, not committed)

Run:

    GH3_MAP=ComptonY|ComptonY_deproj_cib_1.0_10.7 GH3_SAMPLE=kids|kids_z025|g09 [GH3_MUTATE=1] PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 gh3_tsz.py

**Sources:** ACT DR6.02 NILC maps on LAMBDA (https://lambda.gsfc.nasa.gov/product/act/act_dr6.02/act_dr6.02_nilc_info.html);
Coulton et al. 2024, PRD 109, 063530; Zhang et al. 2024, A&A 690, A267.

**Forward note (GH4_tsz_two_halo_compensated):** the compensated, wider-aperture rerun is again NOT DECIDED (Δχ² +3.9). Its
two-halo template proved cuspy, so the two-halo caveat above still stands unquantified.
