# CFG198 — MUSE-DARK per galaxy: a₀(z) from III's own DC14 products, and whether III's rise survives swapping the fitted disc mass for the SED mass (+ H₂). FROZEN CRITERIA

Written 2026-09-29 in the calculation chat, before any CFG198 number. This lane has computed nothing from the per-galaxy files: no a₀ per galaxy, no Δ* against z, and no z-dependence of anything. **κ = ½ FITTED, NOT DERIVED.**

## What was known when this was written

- **The data** (data chat, be78f2054 and f17dae96c): `data_assembly/musedark_catalogues/musedark_numeric.csv`, 126 galaxies, parsed from the MUSE-DARK site's DC14 run files. No definition is shipped with the files, so every definition below is marked as read.
- **Summaries the data chat reported (seen before this commit):**
  - Δ* = DC14 log M_disk − SED log M* over 124 galaxies: median −0.14 dex, 16–84% −0.67 to +0.42.
  - The HI surface density is prior-dominated: the upper 95% limit is ≥ 14 of the prior maximum 15 M☉ pc⁻² for 117 of 126.
  - The `true_Vrot.dat` model extends to a median 6.8 R_e; the papers state the data reach 2–3 R_e.
  - No dependence of anything on z was reported, and this lane saw none.
- **Definitions, as read** (two read-only summaries: Paper I = arXiv:2506.19721, III = arXiv:2604.22613, through a page summariser, unverified against the PDFs):
  - The DC14 run fits X = log(M*/M_vir), with no SED prior on M*. The disc is normalised by that M* and includes molecular gas (Paper I §2.2).
  - The HI is a constant surface density Σ_HI with v ∝ √(Σ_HI r).
  - III's a_bar = disc + HI (+ bulge). Its a_tot = v_c²/r comes from the best-fit DC14 model, with the Dalcanton–Stilp pressure correction. It excludes r < 2 kpc.
  - III's main fit uses 79 galaxies; which 79 is not in these files.
  - III's law (CFG190): a₀(z) = a₀(0) + a₁z, with a₀(0) = 1.0 ± 0.04 and a₁ = 1.59 ± 0.10 (× 10⁻¹⁰ m s⁻²).
- **Hand expectation, disclosed.**
  - The Tacconi-type H₂ scaling adds of order M* at these masses and grows with z.
  - If the DC14 disc does not track it, route (ii) below gets heavier baryons than route (i), increasingly with z. Route (ii)'s a₀(z) would then be flatter than route (i)'s (Δb < 0).
  - How large Δb is, and whether route (i) shows III's rise at R_e at all, I do not know.

## Sample

- Rows of `musedark_numeric.csv` with finite z, `logMstar_phot`, `DC14_logMdisk`, `fDM_at_Re`, `Re_kpc` and `gas_density_Msun_pc2`.
- `has_bulge = 0`. The bulge radius is not in the files, so the 15 bulge galaxies are counted and reported, not analysed.
- 0 < `fDM_at_Re` < 1.
- The count at each step is reported.

## Quantities, per galaxy

- **Geometry (A1, stated approximation):** a thin exponential disc with R_d = R_e/1.678, standing in for the MGE Sérsic disc of aspect 0.15.
  - g_disc(M, R) = v²/R, with v² = (2GM/R_d) y² [I₀K₀ − I₁K₁] and y = R/(2R_d).
  - The evaluation radius is R_e, the radius of `fDM_at_Re`.
- **HI (A2, stated):** g_HI = πGΣ_HI, the enclosed-mass form v² = πGΣr that v ∝ √(Σr) implies. Σ_HI is `gas_density_Msun_pc2` (the posterior median).
- **Route (i) "III's own products":**
  - M_i = 10^`DC14_logMdisk`.
  - g_bar,i = g_disc(M_i, R_e) + g_HI.
  - D_i = 1/(1 − fDM_at_Re).
  - g_obs = D_i g_bar,i. This is the model's data-constrained total at R_e, held fixed in every route.
- **Route (ii) "SED stars + H₂" (primary):**
  - M_ii = M*_SED (1 + μ_mol), with μ_mol the main-sequence scaling as coded in CFG90: 10^(0.06 − 3.3 (log(1+z) − 0.65)² − 0.41 (log M*_SED − 10.7)).
  - g_bar,ii = g_disc(M_ii, R_e) + g_HI.
  - D_ii = g_obs/g_bar,ii.
- **Route (iii) "SED stars only" (variant):** M_iii = M*_SED.
- **Implied a₀ per route:** a₀ = g_bar/y*, where ν(y*) = D.
  - Kernel: ν_mono, CFG4_common's FP1 table (the user's 09-26 kernel). Variant: ν_RAR.
  - Defined only for D > 1.05. The inversion is ill-conditioned as D → 1. Galaxies with D ≤ 1.05 are counted per z-half and per route: for route (ii), D ≤ 1 means the SED + H₂ baryons meet or exceed the model's total.
- **P1:**
  - Δ* = log M_i − log M*_SED against z.
  - Δ* − log(1 + μ_mol), i.e. "fitted disc vs SED + H₂", against z.

## Statistics

- **Slope:** b_r = the Theil–Sen slope of log₁₀ a₀,r on z (dex per unit z).
  - Its 95% CI comes from 10,000 bootstrap resamples over galaxies (seed 198; 2.5/97.5 percentiles).
  - The paired Δb = b_ii − b_i is computed on the galaxies defined in both routes.
- **Reference slopes:** the OLS slope of log₁₀ L(z) on z over the analysed galaxies' own z, for:
  - flat, L = 1;
  - the rival, L = E(z), flat ΛCDM with Ω_m = 0.315;
  - III's law, L = 1 + 1.59z.
- **P1 slopes:** Theil–Sen slopes of the two P1 quantities on z, with bootstrap CIs.
- **Reported, not graded:**
  - the median log₁₀ a₀,r in each z-third, against the two footings (9.36 × 10⁻¹¹ and 1.131 × 10⁻¹⁰ m s⁻²);
  - Spearman ρ of a₀,r with z, with the D ≤ 1.05 galaxies placed at the bottom rank.

## Decision rows (95%)

- **R0 (closure, route i).** Does b_i's CI contain III's reference slope?
  - Yes: the per-galaxy R_e reconstruction from III's own products is consistent with III's rise.
  - No: it is not. Routes are then compared without any claim to reproduce III.
- **R1 (route ii, primary).** Which of flat, E(z) and III's law lie inside b_ii's CI (not excluded), and which lie outside (excluded)?
  - If route (ii) leaves fewer than 30 galaxies with D > 1.05, R1 is NON-DIAGNOSTIC (baryon overshoot), and the overshoot count per z-half is the result.
- **R2 (circularity).** Does Δb's CI exclude 0?
  - Yes: the fitted-mass route changes the a₀(z) slope. Its direction and size are reported.
- **Robustness (reported).** R0–R2 are repeated for:
  - Σ_HI = 0 and Σ_HI = 15 (the prior bounds; they also cover a factor ~2 in A2's coefficient);
  - μ_mol × 0.5 and × 2;
  - ν_RAR;
  - route (iii).
  - A verdict is called robust only if it is the same across all of these. Otherwise it is "gas- or H₂-dependent", as on the KURVS front.
- **Grading.** Nothing here is graded as support for the framework. If route (ii) excludes flat, that is reported plainly as a failure of the flat law on this route, with the caveats.

## Variant (reported): the v22 route

- g_obs = v22²/(2.2 R_d) at 2.2 R_d, reading `v22` as v_c there (A3, unverified).
- Every route's g_bar uses the same geometry at 2.2 R_d.
- b_r and R1 are repeated.
- The consistency of the two g_obs estimates is reported, not graded: the ratio (v22²/2.2R_d) / g_obs(R_e), per galaxy, with its median and 16–84% range.

## Controls

- **C1:** the exponential disc. The peak of y²[I₀K₀ − I₁K₁] lies at R/R_d ∈ [2.1, 2.3], with v²_max R_d/(GM) = 0.3877 ± 0.001. At R = 50 R_d, v² R/(GM) = 1 within 0.5%.
- **C2:** the kernel round trip. ν(y*(D)) = D to 1e-9 for D ∈ [1.06, 100], for ν_mono and ν_RAR.
- **C3:** route identity. With M*_SED := M_i and μ_mol := 0, route (ii) equals route (i): every a₀ ratio is 1 to 1e-12.
- **MUTATE=1:** log M_i → log M_i − 0.4 (z − median z).
  - b_i must rise by ≥ 0.1 dex per unit z, and Δb must fall by ≥ 0.1. The machinery must respond to an injected fitted-mass drift.
  - Outputs are written separately (`*_MUTATE`).
