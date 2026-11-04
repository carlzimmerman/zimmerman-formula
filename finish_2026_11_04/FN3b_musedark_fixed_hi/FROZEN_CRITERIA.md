# FN3b_musedark_fixed_hi: frozen criteria

Committed alone, before any script or number. A new lane after FN3 (`../FN3_musedark_law_refit/`, NOT DECIDABLE WITH THE EXISTING CUBES), written at the owner's "you must find a way" (2026-11-04). It reuses FN3's engine, sample, band, footings, budget terms, readings and grader. kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework. No cold component, no particle.

**Not blind.** FN3's K2' and grader dry run were read first: with Sigma_HI free in [0, 15], the stellar mass trades against HI, a planted rise of 0.60 per unit z comes back as 0.32, and a rise of the survey's size grades BAND CONSISTENT.

## 1. What changes from FN3, and why
FN3 let the HI surface density float over the survey's prior, 0-15 Msun/pc^2. That freedom absorbed the signal. FN3b fixes the HI term from what is measured about HI discs, with its error carried in the budget:
- **Local HI discs follow a tight mass-size relation**, log D_HI = 0.506 log M_HI - 3.293 (D_HI in kpc at the 1 Msun/pc^2 isophote; Wang et al. 2016, scatter about 0.06 dex; from memory, PROVISIONAL). It makes the mean HI surface density inside D_HI nearly independent of M_HI, about 3.7-3.8 Msun/pc^2. Inner discs sit above the mean, and the HI-to-H2 transition caps HI near 9-10 Msun/pc^2 at solar metallicity (Bigiel et al. 2008; PROVISIONAL), higher at lower metallicity.
- **At z ~ 1, 21-cm stacking finds the average HI mass about equal to the stellar mass:** (1.19 +- 0.26) x 10^10 Msun for 7,653 star-forming galaxies at 0.74-1.45 (Chowdhury et al. 2020, arXiv:2010.06617; read from a search summary, PROVISIONAL), about 3 times the local value at the same stellar mass (GMRT-CATz1, arXiv:2207.00031; PROVISIONAL). If the mass-size relation holds there, extra HI widens the disc rather than raising its inner surface density.
- **So FN3b fixes Sigma_HI = 6.0 Msun/pc^2** in the constant-Sigma gas term, for every galaxy and redshift. Per-galaxy scatter is 0.15 dex, random. The common-mode error is 0.25 dex (3.4-10.7 Msun/pc^2), covering the inner-to-mean ratio, the transition cap and an unmeasured change of HI structure with redshift. A redshift trend in Sigma_HI is limited to 0.10 dex per unit z in the slope budget. The assumption is stated: z ~ 0 HI structure carried to z ~ 1.

Everything else is FN3's: the engine (`fn3_cube.py`, conventions of FN3's amendment A1), the sample (`fn3_sample.json`, 71 primary, thirds 23/24/24), the band (CFG689), footings, H2 (Tacconi 2020), the SED budget, readings R0-R2 and R5-R7, and the label rules of FN3's section 7. FN3's R3 and R4 (Sigma_HI 0 and 15) are replaced by **R3b, Sigma_HI x 10^-0.25**, and **R4b, Sigma_HI x 10^+0.25**.

## 2. Budget, recomputed before any data
sigma_cm per third = sqrt(0.20^2 + (L_H2 x 0.10)^2 + (L_band x sigma_band)^2 + (L_HI x 0.25)^2). L_HI = dDelta/dlog(Sigma_HI) is computed like FN3's levers, on the same synthetic galaxies. The slope budget gains (L_HI x 0.10) in quadrature. Both are written to `budget_fn3b.json` before any Stage 1 run.

## 3. K2'' (synthetic, before any data), fresh seeds
- Templates: the 71 primary galaxies, as FN3's K2'. Noise matched-filter S/N 30. New seeds: noise 40261105 + id; draws 50261105 + id.
- Planted Sigma_HI per galaxy: 6.0 x 10^N(0, 0.15). Fitted with Sigma_HI fixed at 6.0 (the lane's rule).
- Scenarios: flat (Delta = 0) and rising (Delta = 0.6 (z - median z)), as K2'.
- Lines: (a) abs(median bias) <= 0.07 dex in every third, flat; (b) flat slope within 0 +- 0.10 per unit z; (c) rising slope within 0.60 +- 0.10; (d) MUTATE a0 x 2 shifts the median Delta by -0.30 +- 0.07; (e) **power: FN3's grader, with FN3b's budget, must not label the rising scenario BAND CONSISTENT** on either footing.
- If any line fails, FN3b issues no label, and no cutout is requested.

## 4. Stage 1 (only if K2'' passes, and only after the owner's yes for FN3's cutouts)
FN3's `fn3_fetch.py --approved` and `fn3_stage1.py`, with Sigma_HI fixed at 6.0 in R0 and the readings above. Labels and flags as FN3's section 7, with [GAS-DEPENDENT] set by R3b, R4b, R5-R7.

## 5. What a label here can say
A label rests on the stated HI assumption. BAND CONSISTENT or BAND EXCLUDED holds only if z ~ 1 HI discs keep the local mass-size relation to within 0.25 dex in inner surface density. It is not a measurement of a0(z).
