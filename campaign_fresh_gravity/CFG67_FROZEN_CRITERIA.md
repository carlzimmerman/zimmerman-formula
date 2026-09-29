# CFG67 — the ΛCDM control for CFG61 (the KiDS early/late split): FROZEN CRITERIA

Written 2026-09-29, **before any CFG67 script exists and before any ΛCDM prediction for these data has been computed**. This file is committed on its own. This follows the repo's control pattern (CFG23, CFG25): standard halos run through exactly the same machinery.

## Question

CFG61 found that the KiDS-1000 early-minus-late lensing difference rejects B's colour-blind law, and B with its derived rule (identical at KiDS masses), at χ² 28.1 / 7 in the 1-halo bins. **Is that failure specific to a colour-blind dark mass, or generic to the machinery (the class proxies, the reconstructed isolation, the forward model)?** Does standard ΛCDM, run through the same machinery, reproduce the difference?

## Identical to CFG61 (executed read-only from `CFG61_kids_colour_split.py`)

- **Data:** Brouwer+2021 Fig. 8 colour bins and their 30×30 covariance.
- **Lenses:** `lr_lenses.npz` (the class proxies, M_gal, z).
- **Forward model:** R = √(G M_gal / g), weight 1/g within a bin and M_gal across lenses.
- **The projector.**
- **K1:** the seven 1-halo bins (lens-weighted median R < 0.3 Mpc for both classes).
- **The ±0.1 dex early-class stellar-mass floor**, applied as a shift of the true mass at the tabulated R.

## The ΛCDM comparator (no free or tuned parameter)

- **ΔΣ = ΔΣ_point(M_gal) + ΔΣ_NFW(M_200c):** the stellar and cold-gas point mass plus an NFW halo. The halo stands for the total halo mass as lensing measures it; any double-count of the ~3% of mass in stars is accepted and noted.
- **HEADLINE: colour-split stellar-to-halo relation.**
  - M_200c = CFG36's `collapse(M_*, colour)`, which is Mandelbaum+2016's measured red and blue halo masses converted to M_200c. Red is used for the early class, blue for the late one.
  - Concentration is Dutton–Macciò, as in CFG36's `nfw_enclosed`. The enclosed mass is taken as implemented there, saturating at 5 R_200c.
  - M_* = 10^logM.
  - Below Mandelbaum's measured range (log M_* < 10.28 red, 10.24 blue) `collapse` clamps (the standing artefact). The M_gal-weighted fraction of lenses below the range is reported.
- **Reported variant: colour-blind stellar-to-halo relation.** CFG35's Moster+13 `halo_mass(M_*)` for both classes.
- **Caveat, stated up front:** the colour-split relation is itself calibrated on SDSS lensing. A pass is therefore consistency between the SDSS and KiDS colour splits under standard halos, not a first-principles ΛCDM prediction. The colour-blind variant is the a-priori version.

## Statistic

- **The measured and predicted differences on K1:** D_obs = d_early − d_late, with C_D = C_ee + C_ll − C_el − C_le. D_Λ is ΛCDM's predicted difference.
- **Goodness of fit:** χ²_Λ = (D_obs − D_Λ)ᵀ C_D⁻¹ (D_obs − D_Λ), with 7 degrees of freedom.
- **Amplitude:** D_obs ≈ A · D_Λ. A = 1 is ΛCDM; A = 0 is a colour-blind prediction (as CFG61's law gives, D_L ≈ 0).
  - Â = D_Λᵀ C_D⁻¹ D_obs / D_Λᵀ C_D⁻¹ D_Λ.
  - σ_A combines the statistical error with half the spread of Â under the ±0.1 dex early-class floor.

## Pre-declared checks

- **C1 CONTROL:** CFG61's committed law χ²_L = 28.1 / 7 (canonical) reproduced by the executed machinery to ±0.1.
- **C2 CONTROL:** CFG36's NFW gives M(<R_200c) = M_200c to 1e-6, and the projector reproduces Wright & Brainerd's untruncated NFW to 1e-3.
- **H1 [HEADLINE; MUTATE must fail]:** ΛCDM with the colour-split relation reproduces the difference: χ²_Λ with p > 0.01 **and** |Â − 1| < 2σ_A.
- **H2:** the data prefer ΛCDM's split over a colour-blind prediction: Â / σ_A > 3.
- **H3 (reported):** the absolute profiles on K1 against ΛCDM (early with C_ee, late with C_ll).
- **Reported rows:**
  - R1: the colour-blind Moster variant (D, χ², Â).
  - R2: the Sérsic replicate.
  - R3: all 15 bins, out of the isolation-reliable range, with no 2-halo term.
  - R4: the clamped weight fraction.
- **MUTATE:** swap the early and late data (the profiles and the covariance blocks). H1 must fail and the script must exit 1.

## Reading (declared)

- **H1 PASS:** standard halos with the measured colour-split halo masses reproduce the KiDS split through the same machinery. **CFG61's failure is specific to a colour-blind dark mass**, not an artefact of the machinery.
- **H1 FAIL:** ΛCDM with measured halos also misses. CFG61's failure is not (only) framework-specific: the class proxies, the reconstructed isolation or the forward model share the blame. H2 and R1 say how.

κ = ½ and Ω_c h² stay fitted. Nothing here says the theory is closed.
