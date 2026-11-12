# EUC1 (ECLIPSE SATURATION CEILING): FROZEN CRITERIA

Committed alone, before any EUC1 script exists and before any EUC1 number is computed. 2026-11-12.

κ = ½ FITTED. Footings 9.3603e-11 (canonical) / 1.132e-10 (alt) m/s², graded separately, never pooled. Not "theory
closed". No outcome of this lane may be described as the data favouring the framework: the test is one-sided and can
only fail the law or leave it standing.

## 0. What this lane is

The framework asserts (`hy4_preview_push/FRAMEWORK.md` §1, (O) and (L)): no second halo, light and matter both feel the
clock sector's density, and the cold pull **saturates**: `g_c = a₀ g/(g + a₀) ≤ a₀` (law S), or `g_c ≤ a₀/2` (law B).
A55/A70 graded the projected law against 70 SLACS Einstein radii (source redshifts known): 12 % short in radius,
needing 1.174 ± 0.039 × Salpeter.

Euclid DR1-Foundation (November 2026) released the ECLIPSE strong-lens catalogue: 15,072 grade A/B lenses with
Einstein radii, Sérsic light profiles (measured index and half-light radius), photometric lens redshifts and Salpeter
stellar masses. **It carries no source redshifts.** The repository's review of the release
(`research_closure_2026_11_12/euclid_desi_release_review`) audited the catalogue and ran no physical test on it.

This lane runs the one test that needs no source redshift. For any lens,

    mean total surface density inside the Einstein radius = Σ_cr(z_l, z_s) ≥ Σ_cr,∞(z_l) ≡ Σ_cr(z_l, z_s → ∞).

So `π R_E² Σ_cr,∞(z_l)` is a strict lower bound on the projected mass inside the Einstein radius, whatever the source.
The law fixes the most it can supply from the catalogued baryons. If the bound exceeds the supply by more than any
stellar-mass rescaling can cover, that lens cannot exist under "law + baryons only", for any source redshift.

## 1. Data (frozen)

Public ECLIPSE archive, DOI 10.5281/zenodo.19654904, already on this machine. No other download.

| File | sha256 |
|---|---|
| `ECLIPSE_object_catalogue.zip` | 5486e82867a0209767d542478b5375413f68bc8adf033f157da940b4c6f75438 |
| `ECLIPSE_D_dr1_redshifts_and_physical_properties.zip` | 511b68d3aa00c2289098fe47e251b3e9667fc6ea025083396a9a9ebcda8fb186 |
| `eclipse_dr1_catalogue_key_v20261103.csv` (inside the second) | 65338917534c9c767c4f45732d29937d2dfb7fd68083cdfd05aec994ee4fa9ab |
| `ECLIPSE_object_catalogue.csv` (inside the first) | 8247a4d5f23513b83be6db5a8244234f0cc1e1ac66e4de1a54983ae5984786b2 |

Columns used, key catalogue: `unique_identifier`, `lens_grade`, `eclipse_median_phz`, `eclipse_min70_phz`,
`eclipse_max70_phz`, `eclipse_log_survived_mass_med` (+ `_low`, `_upp`), `eclipse_effective_einstein_radius`
(+ bounds), `eclipse_einstein_radius`, `eclipse_effective_radius` (+ bounds), `eclipse_sersic_index`,
`lens_model_success`, `final_sample`. Object catalogue: `Unique_Identifier`, `large_system_warning`, `disc_deflector`,
`desi_deflector_specz`.

Instrument-check sample: `real_research/data/slacs_auger2009_lenses.tsv` (A55's file; source redshifts known).

**Seen before freezing (disclosed).** The READMEs and column lists; the row counts in the review's metadata audit
(3,202 for the primary cut below); and these summary statements in Nersesian et al.: median log M★ = 11.39 (Salpeter),
mean R_eff = 5.7 kpc, mean R_E = 6.4 kpc, and "at fixed stellar mass the SLACS lenses have smaller Einstein radii than
the Euclid lenses by 0.3 dex". From those three means I made one back-of-envelope estimate for a single typical lens
(supply ≈ lower bound at z_s = ∞). No per-lens ECLIPSE value has been read, plotted or computed. The 0.25 dex margin of
§4 was chosen from the stellar-mass systematics of §4 before that estimate.

## 2. Samples (frozen)

**P (primary):** `lens_grade == 'A'` and `lens_model_success` and `final_sample` and `large_system_warning == False`,
and all of: `eclipse_effective_einstein_radius > 0`, `eclipse_effective_radius > 0`,
`0.6 ≤ eclipse_sersic_index ≤ 10` (the Prugniel–Simien range), `eclipse_median_phz > 0`,
`eclipse_log_survived_mass_med > 0`. Rows removed by the last five conditions are counted and reported.

**S (secondary):** the same with grades A and B.

No lens is removed after its statistic is seen.

## 3. Model (frozen)

**Cosmology:** the catalogue's own (Nersesian et al.): flat ΛCDM, H₀ = 67.74 km/s/Mpc, Ω_m = 0.3089. Its stellar masses
and kpc sizes are in it. Distances by direct numerical integration, radiation neglected.

**Baryons:** a spherical Sérsic body of total mass `M★ = 10^eclipse_log_survived_mass_med`, index
`n = eclipse_sersic_index`, half-light radius `R_e = eclipse_effective_radius × D_A(z_l)`, deprojected with the
Prugniel–Simien form (A55's `M3D_star`). No gas, no halo, no neighbours, no external field. Each omission is discussed
in §7; the external field and the truncation of the phantom field both lower the supply, so leaving them out favours
the law.

**Laws:**
- law S: `g_N = g²/(g + a₀)`, i.e. `g = ½ g_N (1 + √(1 + 4a₀/g_N))`;
- law B: `g² = g_N² + a₀ g_N`.

**Projection:** `M_2D(<R) = (R²/G) ∫_R^{r_max} g dr/√(r² − R²)`, `r_max = 10⁶ kpc` (A55's `M2D_from_g`, Gauss–Legendre
in `r = R cosh u`). Light and matter see the same potential (A12; slip is O(ε²), A55 §2.3).

**Lower bound:** `M_min = π R_E² Σ_cr,∞(z_l)`, `R_E = eclipse_effective_einstein_radius × D_A(z_l)`,
`Σ_cr,∞ = c²/(4πG D_l) × lim_{z_s→∞} D_s/D_ls`, the limit taken at z_s = 1100 (it has converged to < 1 % by then; the
script prints the convergence).

## 4. Statistic and verdict (frozen)

**Per lens:** `b_i = log₁₀ B_i`, where `B_i` solves `M_2D,law(<R_E; B_i M★) = M_min`: the factor by which the
catalogued Salpeter stellar mass must be multiplied for the law to make this lens with its source at infinity. `b_i` is
a **lower bound** on the true required boost; any finite source redshift raises it.

**Margin.** `b* = 0.25 dex` (1.78 × Salpeter, about 2.8–3.2 × Chabrier). Reasons, fixed here: the catalogue's masses
are already Salpeter and already the high estimate (0.23 dex above the Euclid pipeline's own NNPZ masses on the same
photometry); A70 found the SLACS population needs 0.070 dex at the true source redshift; published IMF mismatch for
massive early types reaches about 0.1–0.2 dex above Salpeter at the extreme; per-lens errors (mass ≈ 0.1 dex,
photo-z ≈ 0.07 dex in surface density) add about 0.12 dex. A lens with `b_i > b*` cannot be rescued by the IMF or by
its error bars, for any source redshift.

**Population statistics, per law and footing, on P:**
- `f₂₅` = fraction of lenses with `b_i > 0.25`;
- `f₀` = fraction with `b_i > 0`;
- `b_med` = median `b_i`.
Each with a 95 % bootstrap interval (2,000 resamples of lenses, seed 20261112).

**Verdict word, per footing, read on law S (the law with the larger supply):**
- **CEILING BROKEN** if the lower 95 % bound of `f₂₅` ≥ 0.25;
- **CEILING HOLDS** if the upper 95 % bound of `f₂₅` ≤ 0.10;
- **NO VERDICT** otherwise.

The 0.10 floor is the contamination allowance: catastrophic photo-z outliers (4.3–4.7 % in the paper), false positives
among grade A, residual group-scale systems, and the 2σ tail of the per-lens errors. Law B is reported beside law S; it
supplies less, so it cannot hold where law S breaks.

The lane verdict is the pair canonical / alt.

**What each verdict means.**
- CEILING HOLDS: the Euclid sample does not exclude "law + Salpeter baryons" without source redshifts. It is not a
  pass: A55/A70's shortfall at known source redshift stands, and the conditional readings of §5 say how far the sample
  sits from the realistic case.
- CEILING BROKEN: at least a quarter of Euclid's grade-A, successfully modelled galaxy-scale lenses need projected mass
  inside ~R_E that the law cannot supply from their stars for any source redshift or IMF. Then either galaxy-scale
  lenses carry gravitating density beyond the law's saturating cold pull (assertion (O) "no second halo" fails at this
  scale), or the catalogue's inputs are wrong in a way §6 must locate.
- NO VERDICT: reported as such, with the conditional readings.

## 5. Conditional readings (frozen; reported, never the verdict)

The same statistics with the source placed at a finite redshift instead of infinity:
- **R3:** z_s = 3.0 for every lens (above the 0.3–2.7 range of the DESI-vetted ECLIPSE sources);
- **R2:** z_s = max(2.0, z_l + 0.5).
Lenses with z_l ≥ z_s − 0.2 are dropped from that reading and counted. These are labelled CONDITIONAL on the source
distribution and carry the same thresholds, as "would-be" words only.

## 6. Instrument checks (frozen; any failure makes the lane NOT EVALUABLE)

- **K1** point mass: `M_2D` returns the mass to 10⁻⁶ at a₀ → 0; SIS: constant deflection to 10⁻⁴.
- **K2** A55 reproduction on SLACS at the true source redshifts, a₀ = 1.132e-10, Salpeter, n = 4, Auger cosmology:
  median `R_E,pred/R_E,obs` = 0.885 ± 0.005.
- **K3** A70 reproduction: population boost solving the SLACS median to 1 is 1.174 ± 0.02.
- **K4** twin projection: on 20 lenses of P chosen by fixed row index (every ⌊N/20⌋-th), `M_2D,law` from a direct
  line-of-sight integral of the total density agrees with §3's to 10⁻³.
- **K5** SLACS at z_s = ∞ (reference only, no threshold): the same `b_i` statistics, printed beside the true-z_s ones,
  so the cost of dropping the source redshift is on the page.
- **K6** `M_min` cosmology scaling: H₀ → 70 moves `b_med` by the amount `log(70/67.74)` predicts to 0.01 dex.
- **MUTATE** (`EUC1_MUTATE=newton`, a₀ → 10⁻³⁰): `f₂₅` must rise on both footings and the script must exit 1.
  Outputs under a separate name.

## 7. Robustness (frozen list; reported; cannot change the verdict word)

1. `R_e × 0.80` (the README says the radius is not circularised, the paper says it is; 0.80 is a q ≈ 0.64
   circularisation and raises the supply).
2. `n = 4` for every lens.
3. `eclipse_einstein_radius` (SIE parameter) in place of the effective radius.
4. z_l < 1.0 only; and the lenses with a DESI deflector spectroscopic redshift, at that redshift, with stellar mass
   rescaled by the luminosity-distance ratio squared.
5. Excluding θ_E > 2.5″ (group-scale geometry).
6. Monte Carlo of the catalogued errors (photo-z 70 % interval as ±1.04σ, mass errors, θ_E and R_e bounds), 200 draws:
   the spread of `f₂₅`.
7. Sample S.
8. `r_max = 300 kpc` (a truncated phantom field, the less generous case).

If any of 1–5, 7 moves `f₂₅` across a verdict threshold, the RESULT says so in its first paragraph.

## 8. Map (exploratory; no verdict; labelled as such)

Medians of `b_i` and of the minimum excess surface density `ΔΣ_min = Σ_cr,∞ − M_2D,law(<R_E)/(πR_E²)` (M☉ pc⁻²) in bins
of log M★ (0.2 dex), z_l, θ_E/θ_e and n; the difference in median `b` between the 0.2 dex bins either side of SP1's
switch mass (log M★ = 11.21, reported per footing as SP1 recorded it). SP1 is a sealed weak-lensing prediction of a
retired sector and is **not graded here**. The map is what the sample says about where any extra gravitating density
would have to sit; it is a description, not a test.

## 9. Not claimed

- No measurement of a₀ or κ (lensing does not measure a₀ with the IMF free: A70).
- No statement about clusters or groups; `large_system_warning` systems are excluded.
- No use of the SIE velocity scale as dynamics.
- A HOLDS is not a pass of the lensing gate.
