# CFG61 — does B's derived rule reproduce the KiDS-1000 early/late lensing split? FROZEN CRITERIA

Written 2026-09-29, **before any CFG61 scoring script exists and before any model prediction for this data set has been computed**. This file is committed on its own. Any later deviation goes in the README as a disclosed departure.

**Known before freezing** (reported in the lensing-RAR review, `real_research/reviews/lensing_rar/lr_battery_results.md`): the released profiles show early types above late types, χ² = 119.9 / 15 in u−r (8.8σ) and 69.1 / 15 in Sérsic index (5.8σ). No model of B, or of B's derived rule, has been compared to them.

## Question

B's law is colour-blind: the dark mass is a function of the baryons alone. In the deep regime it predicts the same excess surface density at a fixed baryonic acceleration for any lens mass, so it predicts **no** early/late split. B's derived cold-mass rule (CFG35/36) adds collapse debris whose mass depends on colour (Mandelbaum+2016's red and blue collapse masses).

**Does the rule's colour dependence reproduce the measured split, where the law cannot?**

## Data (on disk; nothing fetched)

- **Profiles:** Brouwer+2021 Fig. 8, `real_research/data/lensing_rar/brouwer2021_rar/Fig-8_RAR-KiDS-isolated_Colorbin_{1,2}.txt`.
  - Bin 1 is u−r < 2.5 (late); bin 2 is u−r ≥ 2.5 (early). Each has 15 bins in g_bar.
  - The covariance is `..._Colorbins_covmatrix.txt`, rebuilt as `reshape(2,2,15,15).transpose(0,2,1,3).reshape(30,30)`.
  - ESD and errors are divided by `bias` (1+K); the covariance by (1+K)².
- **Sérsic replicate (reported only):** `..._Sersicbin_{1,2}.txt` (n < 2 late, n ≥ 2 early).
- **Lens mass distributions:** `real_research/data/lensing_rar/lr_lenses.npz` (181,477 isolated lenses; `Mgal` = M_*(1 + f_cold), Brouwer's g_bar mass; `logM`, stellar; `typ` 1 = early, 0 = late; `z`). This is a derived local product of the committed `real_research/reviews/lensing_rar/lr_esd_remeasure.py`.
- **Declared caveat:** `typ` uses rest-frame LePhare u−r > 2.0, not Brouwer's observed GAaP u−r ≥ 2.5, and the isolation is the repo's reconstruction (181,477 lenses against Brouwer's 259,383). The class mass distributions are therefore proxies. The shift of the median log M_gal between the two class definitions is reported (R3).

## Forward model (identical machinery for both models; both footings)

- **Where each lens sits in a bin:** for lens i and g_bar bin k (edges logspace(1e-15, 5e-12, 16)), the pairs sit at R = √(G M_gal,i / g), g within the bin.
- **Weights across lenses:** pairs per ln g ∝ M_gal,i / g. Within a bin the model is averaged over ln g with weight 1/g. Across lenses the weight is M_gal,i. A Σ_crit⁻² factor for a source plane at z_s = 0.75 is reported as a bracket (R2).
- **Model ESD:** the projected ΔΣ(R) of a spherical enclosed-mass profile, with the referee's own projector (validated in C2). Baryons are a point mass M_gal.
- **L (B's law):** M_L(<r) = M_gal ν_mono(G M_gal / r² a₀) out to the edge r_e = 0.40 r_ta, then frozen (source-confined edge). r_ta is B's committed convention: where the law's own enclosed mass falls to Δ_ta(z) ρ̄_m(z), at the lens redshift, with the top-hat Δ_ta.
- **S (B + derived rule):** M_S = M_L + f_ex (1 − f_b) M_NFW(<r; M_coll), truncated at r_e.
  - The collapse mass is CFG36's `collapse(M_*, colour)` (Mandelbaum+2016, M_200c, Dutton–Macciò concentration), red for the early class and blue for the late one.
  - f_ex = max(0, 1 − M_ph,edge / [(1 − f_b) M_coll]) is CFG35's conservation form at x_e = 0.40.
  - M_* is `10^logM` as tabulated.
- **Not modelled:** the 2-halo term and hot gas (Brouwer's g_bar has none). The headline therefore uses only the **1-halo bins K1**: those where the lens-weighted median R of **both** classes is < 0.3 Mpc, Brouwer's stated isolation-reliable range. K1 is fixed by the lens distribution before any comparison with the profiles.

## Statistic

- **The measured difference:** D_obs = d_early − d_late on K1, with covariance C_D = C_ee + C_ll − C_el − C_le.
- **The predicted differences:** D_L and D_S, the same differences of the model stacks.
- **One amplitude:** D_obs ≈ D_L + A (D_S − D_L). A = 0 is the law; A = 1 is the rule.
  - Â = [ΔᵀC_D⁻¹(D_obs − D_L)] / [ΔᵀC_D⁻¹Δ], with Δ = D_S − D_L.
  - σ_A,stat = (ΔᵀC_D⁻¹Δ)^(−1/2).
- **Systematic floor:** a colour-dependent stellar-mass calibration of ±0.1 dex on the early class (half the spread of Â), added in quadrature to σ_A,stat to give σ_A.
- **Goodness of fit:** χ²_L = (D_obs − D_L)ᵀC_D⁻¹(D_obs − D_L), and likewise χ²_S, with |K1| degrees of freedom.

## Pre-declared checks

- **C1 CONTROL:** the released profiles give the committed split, χ² = 119.9 / 15 (u−r) and 69.1 / 15 (Sérsic) for early vs late on all 15 bins, to ±0.5.
- **C2 CONTROL:** the projector reproduces a point mass (ΔΣ = M/πR²) and an untruncated NFW (Wright & Brainerd closed form) to 1e-3.
- **C3 CONTROL:** lr_lenses.npz has 93,398 late and 88,079 early lenses, with median logM 10.328 and 10.744.
- **C4 CONTROL:** the law's ΔΣ at fixed g_bar ≤ 1e-12 m/s² is mass-independent to within 3% between M_gal = 1e10 and 1e11 (the deep-regime identity that makes D_L ≈ 0), edge excluded.
- **H1:** the colour-blind law is rejected by the split in the 1-halo regime: Â / σ_A > 3 on both footings, equivalently χ²_L with p < 0.0027.
- **H2 [HEADLINE; MUTATE must fail]:** B's derived rule accounts for the split: |Â − 1| < 2σ_A on both footings, and χ²_S with p > 0.01.
- **H3 (reported):** the absolute early-class profile on K1 against S and against L (χ² with C_ee), and the late class against L.
- **Reported rows:**
  - R1: the Sérsic replicate.
  - R2: the Σ_crit⁻² weighting bracket.
  - R3: the class-definition shift (median log M_gal by lr typ).
  - R4: the hot-gas mass fraction the early class would need for the law alone to reach Â.
  - R5: all 15 bins including the 2-halo range, labelled out of the isolation-reliable range.
- **MUTATE:** swap the early and late data (the profiles and the covariance blocks). Â changes sign, and H2 must fail with exit code 1.

## Reading (declared)

- **H1 PASS, H2 PASS:** the KiDS early/late split, an independent survey, is the colour dependence B's derived rule imports from SDSS. B needs the rule; the law alone is rejected.
- **H1 PASS, H2 FAIL:** the law is rejected, and the rule's colour-dependent debris does not reproduce the split either (the size of Â − 1 says by how much and in which direction).
- **H1 FAIL:** in the 1-halo regime, with B's own lens-by-lens model, the split does not reject the colour-blind law.

κ = ½ and Ω_c h² stay fitted. Nothing here says the theory is closed.
