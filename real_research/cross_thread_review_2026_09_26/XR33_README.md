# XR33 — galaxy-scale strong lensing from baryons alone in the chain's law, and the IMF it needs

Cross-thread review, 2026-09-27. Two scripts, a shared module and six transcribed data tables in this folder. Nothing outside
this folder was edited. Both a₀ footings are carried: canonical 9.3603 × 10⁻¹¹ and alt 1.1312 × 10⁻¹⁰ m s⁻². κ = ½ is
fitted (Z = κ = 5.7888), and nothing in this lane derives it. No constant was added.

## The answer

**Partly.** The chain's law reproduces the SLACS Einstein masses and the SLACS velocity dispersions together, from stars
alone, but only with a stellar IMF about 0.1 dex heavier than Salpeter.

- **With a standard IMF, no.** The Einstein mass comes out 80–82% of the observed value with Salpeter and 49–51% with
  Chabrier. The Einstein radius comes out 16% short with Salpeter.
- **The required IMF:** α_Salp = 1.27 (canonical) or 1.25 (alt), which is 2.2 × Chabrier.
- **Against the heaviest spectroscopic IMF:** that requirement sits at the heaviest IMF measured spectroscopically in the
  34-galaxy Conroy & van Dokkum (2012) sample (α_Salp = 1.275). It is 0.11–0.12 dex above their α–σ relation at the lenses'
  σ, while LCDM's own SLACS IMF sits +0.02 dex from it.
- **Dynamics:** with that IMF the aperture dispersions match (σ_pred/σ_obs = 0.99). But they match just as well with a₀ = 0
  and a 0.05 dex heavier IMF. At these radii the dispersions cannot tell the chain's phantom (about 10% of M_E) from a slightly
  heavier IMF.

## The law as applied

- **Lensing = dynamics:** PPN γ = 1 (FP2 L6a, FP7 R7p), so the lensing mass is the dynamical mass.
- **The spherical AQUAL root:** g = g_N + a₀ x_P2(y − y_th), with x_P2(D) = √(D² + D) − D. This is P2 exactly (FP7 A2), with
  FP9's yield.
- **Separator constants:** from FP9's committed results. The band-pass is applied as a line-of-sight cut at 2L(z).
- **Stars:** de Vaucouleurs profile, exactly deprojected, with Auger+2010's rest-frame-V r_e.
- **Lens geometry:** (Ω_m, Ω_Λ, h) = (0.3, 0.7, 0.7), the SLACS tables' own.
- **Treated as brackets:** the external field, gas, the band-pass, the yield, profile shape, h and the dark fluid.

## Predicted against observed lensing masses (SLACS, 59 lenses; 53 non-outliers give the same numbers)

| | canonical | alt |
|---|---|---|
| y_N = g_N/a₀ at R_E (Salpeter) | 10.9 | 9.0 |
| κ̄ = M₂D,pred(R_E)/M_E, Chabrier / Salpeter | 0.490 / 0.804 | 0.505 / 0.822 |
| R_E,pred/R_E,obs, Chabrier / Salpeter | 0.526 / 0.837 | 0.533 / 0.849 |
| **required log α_Salp** (median ± bootstrap) | **+0.105 ± 0.012** | **+0.096 ± 0.012** |
| required log α_Chab | +0.349 | +0.341 |
| phantom share of M_E at that IMF | 9.5% | 11.1% |

The per-lens scatter of log α is 0.107 dex. The median SPS mass error is 0.080 dex.

The record's other kernels, as labelled sensitivities that are not the chain's law and are not pooled with it:
- ν_mono: +0.088 / +0.078
- ν_RAR: +0.096 / +0.087

**Brackets** (shift in the median log α_Salp, canonical footing):

| bracket | shift (dex) |
|---|---|
| band-pass cut (L, 2L, none) | ≤ 1 × 10⁻⁴ |
| yield on/off | ≤ 1 × 10⁻⁴ |
| external field 0.01 / 0.03 / 0.1 / 0.3 a₀ | +0.001 / +0.003 / +0.005 / +0.008 |
| hot gas 2 / 5 / 10% of M* | −0.009 / −0.021 / −0.041 |
| Sérsic n = 3 / 6 | +0.023 / −0.028 |
| r_e ± 3.5% | ±0.010 |
| h = 0.674 | −0.016 |
| dark fluid, f × the Salpeter-LCDM dark mass (f = 0.203 / 0.503) | −0.030 / −0.077 |
| dark fluid, f × Moster+2013 abundance-matched halos (log M₂₀₀ ≈ 14.05) | −0.059 / −0.162 |

- **The external field does not matter.** The phantom it removes lies beyond about 70 kpc and is weighted by R_E²/2r².
- **Dark-fluid brackets.** The two fractions f are XR19's halo-scale residue 1 − F_esc(0): nominal 0.203 and halo-only 0.503.
  The fluid is treated as kernel-invisible (FP10 L11a). The abundance-matched anchor is the Chabrier-LCDM halo that
  Auger+2010 disfavour, so it is an upper bracket only.

**Other samples** (median log α_Salp, canonical / alt):

| sample | N | what it probes | log α_Salp |
|---|---|---|---|
| S4TM (Shu+2017) | 40 | σ ≈ 202 km s⁻¹ | −0.094 / −0.100 |
| BELLS | 22 E | z ≈ 0.52, R_E ≈ r_e | +0.120 / +0.109 |
| SNELLS | 3 | R_Ein 1.5–2.2 kpc, y_N 20–48 | −0.112, −0.057, −0.117 (canonical, per lens) |

- **BELLS** stellar masses are not published. They are calibrated here on SLACS's own SPS masses from F814W (rms 0.057 dex).
  A quadratic calibration gives +0.17 / +0.16, so BELLS carries about 0.1 dex of calibration systematics.
- **SNELLS:** the phantom share at R_Ein is 3.5–6%.

## The IMF the chain needs, against independent IMF evidence

| comparison | canonical | alt | LCDM's own IMF, same test |
|---|---|---|---|
| SLACS − spectroscopic relation (CvD12b: log α_MW = 0.111 + 0.628 log(σ/200), rms 0.12; Salpeter = 1.6) | **+0.118 ± 0.013** (χ²/N 1.06) | +0.110 ± 0.013 | Treu+2010: +0.021 |
| SLACS − ATLAS3D XX dynamics-with-halo relation (Cappellari+2013) | +0.138 | +0.130 | |
| SLACS − Posacki+2015 (lensing + dynamics + halo) | +0.143 | +0.131 | |
| SLACS: chain − Treu+2010 per lens (51 in common) | +0.061 | | |
| S4TM − CvD12b | −0.042 | −0.049 | |
| BELLS − CvD12b (calibration-limited) | +0.21 | +0.20 | |
| SNELLS mean − SLACS at σ ≥ 280 | **−0.256** | −0.253 | **−0.297** |

- **Barnabè+2013 SSP slopes** exist for two SLACS lenses. The chain's per-lens requirement follows them in direction:
  - J0936+0913: slope x = 2.10 ± 0.15 (sub-Salpeter); the chain needs log α_Salp = −0.056.
  - J0912+0029: slope x = 2.60 ± 0.30 (super-Salpeter); the chain needs +0.185.
- **The heaviest CvD12b IMF** is NGC 4552, at α_Salp = 1.275. The chain's SLACS median is 1.273 (canonical), which is the edge.
- **The SNELLS-versus-SLACS pincer is shared with LCDM, and is larger there.** SNELLS lenses probe R ≈ 0.2–0.7 r_e and need a
  lighter IMF than SLACS lenses of lower σ, in both frameworks.

## Joint lensing + dynamics (Jeans; 53 non-outliers; SDSS fibre 1.5″, seeing FWHM 1.5″, isotropic)

**The chain.** With the lensing IMF:
- σ_pred/σ_obs has median 0.989 (canonical) and 0.986 (alt).
- log α_dyn − log α_lens = −0.001 ± 0.011 (canonical) and +0.003 ± 0.011 (alt).
- χ²/N = 2.8 using the σ errors alone.
- At fixed IMF the phantom raises σ by only 2.1–2.6%.

**Brackets** on the median σ ratio:

| bracket | σ_pred/σ_obs |
|---|---|
| β = +0.2 / −0.2 | 1.011 / 0.971 |
| seeing 1.0″ / 1.8″ | 0.992 / 0.987 |
| ν_mono / ν_RAR | 0.983 / 0.983 |
| Sérsic n = 3 / 6 | 0.956 / 1.079 |
| Hernquist stars | 0.945 |
| dark fluid, f = 0.203 / 0.503 | 0.971 / 0.946 |
| S4TM | 1.008 |

**Caveat.** The MUTATE (a₀ = 0, stars only) also passes: its σ ratio is 1.014 and Δ log α = −0.025.

## The LCDM control (stars + NFW) reproduces the published numbers

- **LC1:** an NFW halo with break radius 30 kpc, normalised to M_E, reproduces Auger+2010's projected f_DM inside r_e/2.
  The median |Δ| is 0.026 with Chabrier and 0.029 with Salpeter.
- **LC2:** Treu+2010's per-lens method reproduces their log α lens by lens: +0.018 dex, Pearson r = 0.97.
  - The method: Hernquist stars, isotropic orbits, f* inside the Einstein cylinder with a uniform prior on [0, 1], and the
    posterior median of f*.
  - LCDM's IMF is therefore Salpeter-like, log α_Salp ≈ +0.01 to +0.04.
- **LC3 (reported):** Moster+2013 abundance-matched halos need log α_Salp = −0.17 and under-predict σ (ratio 0.85). This is
  Auger+2010's point that such halos are too massive.

## Controls and MUTATE

- **XR33_lensing_imf:** 13/17 checks pass, 0 load-bearing failures, rc = 0 (50 s).
  - The four failures are pre-declared verdict hypotheses: H1, H3, H4 and H6 fell. H2 and H5 held.
  - C1: the lens geometry reproduces log M_E to 0.001 dex.
  - C2: the Newtonian stars-only limit reproduces Auger+2009's f*M_E to 0.05% (rms 0.004 dex). This also explains the record's
    h53 "validation B" offset (−8%/+12%): h53 used observed-band radii, while Auger used r_e interpolated to 5500 Å.
  - C3: the record's own spherical MOND lensing solver (h53, committed f33d4e86a), re-typed, reproduces its committed numbers
    exactly: 1.168, 0.825, 1.136, 0.794, 0.840. This lane's integrator on the same inputs agrees to 0.006%.
  - C4: FP7's closed form, FP9's committed y_th(z) and L(0), and XC4's splice point y* = 2.3374124053 are all reproduced.
  - C5: numerics agree to 1 × 10⁻⁵.
  - C6: SNELLS's own "no dark matter" α is reproduced.
- **XR33_jeans_lcdm:** 7/7 checks pass, rc = 0 (140 s).
  - V1: the analytic Jeans test agrees to 8 × 10⁻⁵.
  - V2: the record's own Jeans solver (h53 item 54b), re-typed, reproduces 0.856 / 0.955 / 0.824 / 0.934.
  - LC1 and LC2 pass.
- **MUTATE** (a₀ → 0 everywhere, both runs rc = 1):
  - XR33_lensing_imf: C3, C3b, P1 and H2 fail. An a₀-free law needs α_Salp = 1.42, above every spectroscopic IMF.
  - XR33_jeans_lcdm: V2 and P2 fail.
  - The MUTATE runs were made before the main runs, which were made last.

## Pre-declared hypotheses (thresholds fixed in the docstrings before the first full run)

| hypothesis | test | result |
|---|---|---|
| H1 | κ̄ ∈ [0.9, 1.1] with Chabrier or Salpeter | **fell** (0.80–0.82 Salp) |
| H2 | required α_Salp ≤ 1.275 (heaviest spectroscopic IMF) | **held**, at the edge (1.273 / 1.248) |
| H3 | SLACS offset from CvD12b within ±0.10 dex | **fell** (+0.118 / +0.110) |
| H4 | SNELLS not below SLACS (σ ≥ 280) by more than 0.10 dex | **fell** (−0.26); LCDM fails it too (−0.30) |
| H5 | S4TM offset within ±0.10 dex | **held** (−0.04 / −0.05) |
| H6 | BELLS offset within ±0.15 dex (reported only) | **fell** (+0.21 / +0.20), calibration-limited |
| H7 | chain joint σ ratio ∈ [0.95, 1.05] | **held** (0.989 / 0.986), but a₀ = 0 also holds |

## Disclosures

1. The record's committed h53/h54 SLACS result was read before the hypotheses were written. It used the ν_RAR kernel and found
   κ̄_Salp = 0.79–0.85 and R_E 14–18% short.
2. The machinery was smoke-tested in the session scratch. That covers the deprojection, projection, Jeans and h53 re-typing,
   and the SLACS X r_e validation behind C2.
3. The first full run of each script went to the session scratch as a code test. Its results were seen.
   - XR33_lensing_imf: one crash was fixed (a scalar index in C3b).
   - After that run, the dark-fluid bracket was re-anchored. It had used abundance-matched halos; it now uses the dark mass
     LCDM lensing requires at a Salpeter IMF, with the abundance-matched anchor kept as the upper bracket.
   - LCDM's own IMF was added to the same tests, so that a shared failure is visible.
   - XR33_jeans_lcdm: LC2 first failed (+0.077 dex, r = 0.92). It had been implemented as a point estimate, pinned at f* = 1 for
     35 of 51 lenses. It now implements Treu+2010's stated estimator, the posterior median under a uniform prior.
   - No threshold was changed.
4. H2 passes by 0.002 in α_Salp (canonical), far inside the systematics. The Sérsic n = 3 bracket alone would flip it.
5. BELLS stellar masses are this lane's own calibration, not published values.

## Limits

- **Spherical models throughout.** In an elliptical lens AQUAL differs from the algebraic law. FP7 A3 bounds that difference at
  0.035 dex for thin discs; flattened ellipticals are not computed here.
- **The IMF scales are converted, not re-derived.** Salpeter − Chabrier = 0.25 dex (Auger's scale); CvD's "Salpeter ≈ 1.6"; and
  SNELLS's "Salpeter = 1.55". About 0.02 dex of convention slop remains.
- **SPS zero points** are uncertain at about 0.05–0.1 dex. That is comparable to the H3 offset.
- **Galaxy-environment external fields** are bracketed, not measured per lens.

## Files

- `XR33_common.py`: the shared module. It holds the cosmology, the exact Sérsic deprojection, the kernels (P2, ν_RAR, ν_mono),
  the projection, the α and R_E solvers, NFW/DM14/Moster+2013, the Hernquist profile and the aperture Jeans solver.
- `XR33_lensing_imf.py` (part 1), with `.out`, `_MUTATE.out`, `_results.json` and `_results_MUTATE.json`.
- `XR33_jeans_lcdm.py` (part 2), with the same four output files.
- Transcribed data, each file carrying a provenance header:
  - `XR33_data_slacsX_auger2010_table1.tsv`: Auger+2010, ApJ 724, 511.
  - `XR33_data_treu2010_table1.tsv`: Treu+2010, ApJ 709, 1195.
  - `XR33_data_s4tm_shu2017.tsv`: Shu+2017, ApJ 851, 48 (VizieR).
  - `XR33_data_bells_brownstein2012.tsv`: Brownstein+2012, ApJ 744, 41.
  - `XR33_data_snells_smith2015.tsv`: Smith, Lucey & Conroy 2015, MNRAS 449, 3441.
  - `XR33_data_cvd12b_table2.tsv`: Conroy & van Dokkum 2012, ApJ 760, 71.
- The SLACS base table is the record's `real_research/data/slacs_auger2009_lenses.tsv` (Auger+2009, ApJ 705, 1099), read only.

## Reproduction (from the repository root; at most 2 threads)

```
MUTATE=1 python3 real_research/cross_thread_review_2026_09_26/XR33_lensing_imf.py   # rc = 1 by design (~1 s)
MUTATE=1 python3 real_research/cross_thread_review_2026_09_26/XR33_jeans_lcdm.py    # rc = 1 by design (~2 min)
python3 real_research/cross_thread_review_2026_09_26/XR33_lensing_imf.py            # ~1 min
python3 real_research/cross_thread_review_2026_09_26/XR33_jeans_lcdm.py             # ~2.5 min
```
