# MUSE-DARK: a published a0(z) evolution claim at z ~ 0.3–1.4 and the neighbouring bTFR result (data front, 2026-09-29)

Read from arXiv abstract pages and, for MUSE-DARK-III, its arXiv HTML methods text (via a page summariser, so quotes are the summariser's, not checked against the PDF). Nothing downloaded; no author contacted. **Not a calculation and not a verdict.**
Standing rules: a fail is verified as hard as a win; nothing here says the theory is closed or that the data favour any law.

## The claims (abstract level)
| paper | what is stated |
|---|---|
| **MUSE-DARK-III**, Ciocan, Bouché, Fensch, Krajnović, Freundlich, Desmond, Famaey & Techi, arXiv:2604.22613 (A&A 709, L16, 2026) | 79 star-forming galaxies at 0.33 < z < 1.44 (complete above M* > 10^8.8), disk–halo decomposition with stellar, gas and dark-matter components and pressure-support correction from 3D forward modelling; a₀(z~1) = 2.38 ± 0.1 × 10⁻¹⁰ m/s²; a₀(z) = a₀(0) + a₁z with a₁ = 1.59 ± 0.1 × 10⁻¹⁰ m/s²; "statistically significant redshift evolution" |
| **MUSE-DARK-II**, Jeanneau, Richard, Bouché, Krajnović, Ciocan, Freundlich, Epinat & Contini, arXiv:2603.28856 (A&A 709, A120, 2026) | 95 rotationally supported lensed star-forming galaxies at z ~ 1; the baryonic Tully–Fisher zero point shows "no detectable evolution", Δ = 0.00 (+0.06, −0.06) dex relative to the local relation; the abstract says increased cold gas at higher redshift offsets stellar evolution |
| **MUSE-DARK-I**, Ciocan et al., arXiv:2506.19721 | the 127-galaxy parent sample (0.3 < z < 1.5, 8 < log M* < 11), rotation curves to 2–3 R_e; 89% with DM fractions > 50%; 66% with inner slope γ < 0.5 |

## What MUSE-DARK-III's method says (HTML methods text; summariser)
- **Baryons are not measured.** Stellar mass "is not fixed by photometric priors. Instead, it is dynamically inferred in our 3D forward modelling." Gas: "a parametric model which assumes a constant HI surface mass density" (alternatives explored in an appendix).
- **Pressure support:** Dalcanton & Stilp (2010), v_c² = v_⊥² + v_AD²; the dispersion value used was not stated in the text read.
- **Accelerations:** in m/s² (not normalised to R_e); measurements within r < 2 kpc are excluded from the fits; the sample "predominantly probes the low-acceleration regime" (low-mass, DM-dominated galaxies).
- **Fit:** marginalised normal regression (the Roxy package) with a fixed interpolation function (Eq. 1) and uniform priors on log a₀ (−15 to 5) and on the intrinsic scatter (0–3 dex); data split into four quantile redshift intervals of roughly equal number; exact bin boundaries and counts not stated in the text read. Scatter ~0.17 dex, larger than the local ~0.11 dex, attributed to redshift range and poorer data quality; robustness tested with alternative DM profiles.
- **Data:** the paper says the catalogues, including rotation curves, are on the DARK website. The MUSE UDF sample page (dark-matter.osu-lyon.fr) lists, without sizes, for 126 galaxies: best-fit catalogues for seven models (baryons-only, NFW, Burkert, DC14, cNFW, Einasto, Dekel–Zhao), a photometry catalogue, and per-galaxy observed rotation curves, decomposition, input cubes, line maps and mass maps. Lensing-cluster cubes (36 galaxies) and a 212-galaxy MUSCATEL sample (Paper IV, in prep) are at external links (not opened).

## Points for whoever weighs this (inferences are mine)
1. This is a direct published a₀(z) claim in the decisive redshift range, and its sign is a **rise** with redshift. Neither reading (flat a₀ or a₀ ∝ H(z)) is tested here: with a₀(z) = a₀(0) + a₁z, the quoted numbers give a₀(0) = 2.38 − 1.59 = 0.79 × 10⁻¹⁰ at z = 1 by the linear form (the z = 0 intercept of their fit, below the local value used elsewhere), i.e. a factor ≈ 3 rise to z ≈ 1, larger than H(z)/H₀ ≈ 1.8 in ΛCDM at z = 1. Whether the intercept is fitted or anchored is not stated in the abstract.
2. **Circularity risk to be checked in the tables, not assumed:** the stellar mass is a free parameter of the same fit as the DM halo, and the gas is a fixed-HI-profile model, so g_bar and g_obs come from one model rather than from independent baryon measurements. The RAR built that way can shift with the halo profile family (seven are provided), which the authors test in appendices.
3. **The same collaboration's bTFR at z ~ 1 shows no evolution:** Δ = 0.00 (+0.06, −0.06) dex (MUSE-DARK-II). If a₀ ∝ H(z), then at fixed velocity the baryonic mass should be lower by log E(z) ≈ 0.25 dex at z = 1 (mine; assumes the bTFR zero-point offset is in log M_b at fixed V, which I did not check); the abstract's interpretation is that extra gas offsets stellar evolution. The two results are not obviously consistent with each other at the abstract level; how they reconcile is a question for the papers' bodies.
4. **Independent tests already in the record:** the KROSS/KGES z ≈ 1 bTFR (Tiley+2019, in `high_z_tf_tables/`), the MIGHTEE-HI z > 0.25 bTFR (`mightee_hi_highz/`, consistent with local) and PHIBSS2 (`phibss2_z05_08/`) bear on the same question with measured gas.

## What could be done (needs the owner's go each time)
- Read MUSE-DARK-III's tables and figure data from its arXiv HTML page (the same route as GOODS-ALMA and MIGHTEE-HI) to see the per-galaxy accelerations and the redshift bins.
- Read the MUSE-DARK-II tables (four tables) for the bTFR sample.
- Download the catalogue text files from the DARK site (sizes not stated on the page).
