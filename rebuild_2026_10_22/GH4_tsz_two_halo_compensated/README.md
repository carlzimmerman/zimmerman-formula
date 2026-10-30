# GH4_tsz_two_halo_compensated

**Question.** GH3 left the extent of the hot gas around the 88k KiDS isolated lenses (bins 3–4) NOT DECIDED on ACT DR6
CIB-deprojected y, with a lean to gas past R_vir that was unprotected against the two-halo tSZ and large-scale offsets.
Does the lean survive a compensated aperture and an empirical two-halo template? Criteria were frozen first (f5c49ae6a7).

## Verdict

**CIB-deprojected (PRIMARY): NOT DECIDED.** Δχ²(k=1 − k=3) = +3.9 against the frozen threshold of 4. The difference from
GH3's 4.0 means nothing: the lean neither strengthened nor went away. **Standard ILC: NEITHER FITS** (CIB-dominated, as in GH3).

y × 10⁸, compensated (mean of [12, 20) R_vir subtracted), 87,560 lenses:

| x = R/R_vir | [0, .5) | [.5, 1) | [1, 1.8) | [1.8, 3) | [3, 5) | [5, 8) | [8, 12) |
|---|---|---|---|---|---|---|---|
| **CIB-deprojected** | 0.34 ± 2.42 | 0.81 ± 2.04 | 1.25 ± 1.98 | 1.13 ± 1.72 | −1.41 ± 1.35 | −0.96 ± 0.96 | 0.26 ± 0.55 |
| standard ILC | −2.75 ± 1.99 | 0.39 ± 1.88 | 3.72 ± 1.84 | 4.47 ± 1.37 | 1.13 ± 0.94 | 0.06 ± 0.64 | −0.10 ± 0.42 |
| gas to 1 R_vir | 1.17 | 0.87 | 0.39 | 0.06 | 0.00 | 0.00 | 0.00 |
| gas to 1.8 R_vir | 2.26 | 1.86 | 1.05 | 0.26 | 0.01 | 0.00 | 0.00 |
| gas to 3 R_vir | 3.18 | 2.80 | 2.00 | 0.90 | 0.11 | 0.00 | 0.00 |

| CIB-deprojected fit | k = 1 | k = 1.8 | k = 3 |
|---|---|---|---|
| **PRIMARY** (A = 1, b ≥ 0, T_n), χ²/6 | 16.2 (p 0.013) | 15.1 (p 0.020) | **12.3 (p 0.056)** |
| b ≡ 0, χ²/7 | 16.2 (p 0.023) | 15.1 (p 0.035) | 12.3 (p 0.092) |
| free A, with b | 1.81 ± 1.86 | 1.19 ± 0.86 | 1.26 ± 0.56 |

The T_m template gives the same χ² to the shown precision and the same class. Null χ² is 17.2/7 (p 0.016).

## What it shows

1. **The upgrade did not decide it.** Errors barely changed, because the same lenses and the same map set the noise.
   Compensating removes offsets; it does not add signal. Gas to 3 R_vir still fits best, at A = 1.26 ± 0.56 (consistent
   with Zhang's normalisation), but not by enough.
2. **The two-halo term is not what drives the lean, as far as this template can tell.** Its amplitude takes χ² down by
   < 0.1 at every k and is exactly 0 at k = 3.
3. **That is weaker than it sounds: the template failed its own premise.** The criteria expected a smooth template with
   an isolation hole. Measured, it is cuspy (uncompensated 0.111 at x < 0.5, falling to 0.001 by [5, 8)): close
   companions and photo-z neighbours pile up inside R_vir. That shape does not resemble a smooth large-scale pressure
   pedestal, so **b ≈ 0 is not a measurement that the two-halo tSZ is small.** No two-halo correction from a predicted
   amplitude was made: that needs a power spectrum and a halo model, excluded here as non-native inputs.
4. **All models fit only marginally on PRIMARY.** The deficit at 3–8 R_vir (about 1σ per annulus) is not in any model.
5. **Systematics are at the level of the signal.** Bins 1–2 (82,352 lenses, no gas model) stack uniformly negative on the
   deprojected map: −2.8 to −4.6 × 10⁻⁸ out to 8 R_vir, uncompensated (compensated null p 0.107, so not significant).
   The bins 3–4 models differ by 1–3 × 10⁻⁸, so a lens-correlated over-subtraction by the fixed-SED deprojection cannot be
   excluded. A positive y cannot come from it, but the amplitude comparison can shift.
6. **"All 180k lenses" was not delivered as a graded sample.** Zhang+24 has no hot-CGM measurement below the MW-mass bin,
   so bins 1–2 have no prediction; adding them would only dilute the test.

**For the theory:** the hot gas at 1–3 R_vir that route E needs (GH2: k* ≈ 1.8) stays neither confirmed nor excluded.
ACT DR6 stacking on these lenses has reached its limit for this question; repeating it with other apertures would be
hunting. A decision needs a deeper measurement, not another cut of this one. κ = ½ FITTED; c_f EXTERNAL; cold dark energy
is a gravitating field component, never a particle; not theory closed; nothing here says the data favour the framework.

## Checks (all PASS)

- **K1:** β = 2/3 projection, −6.5e-5.
- **K2:** GH3's stamp, annuli and validity rule reproduce GH3's committed Y exactly (max rel diff 0), on both maps.
- **K3:** pixel geometry vs WCS, 7e-11 px.
- **K4:** template on random positions, max |T_n|/σ 1.65.
- **MUTATE:** random positions as lenses give a null (χ² 4.0/7, p 0.78).

## Disclosures

- numpy's `@` emitted divide/overflow/invalid RuntimeWarnings on the jackknife covariance. Recomputing PRIMARY with
  `einsum` under `-W error::RuntimeWarning` matched errors to 2e-16 and χ² to 1e-13, so they are spurious. That check was
  run from a scratch copy and is not committed.
- K2 is the criteria's reworded version, changed before the criteria commit. It needs GH3's float32 annulus means
  (`exact3`), used only there.
- Bins 1–2 lose 11 % of stamps to the footprint and validity rule, against 1.5 % for bins 3–4. Not investigated, since
  they are ungraded.
- 1 lens was dropped by the 20 R_vir < 39′ rule.

## Files

- `FROZEN_CRITERIA.md`, `gh4_tsz2h.py`
- `gh4_{map}_{sample}{,_MUTATE}.out`, `gh4_results_*.json`
- Data: `_external_data/act_dr6_nilc/` (as GH3), the KiDS bright sample in `real_research/data/lensing_rar/`

Run (~4 min, one thread, peak RSS 1.8 GB):

    GH4_MAP=ComptonY_deproj_cib_1.0_10.7|ComptonY GH4_SAMPLE=b34|b12 [GH4_MUTATE=1] PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 gh4_tsz2h.py

**Sources:** ACT DR6.02 NILC maps on LAMBDA (https://lambda.gsfc.nasa.gov/product/act/act_dr6.02/act_dr6.02_nilc_info.html);
Coulton et al. 2024, PRD 109, 063530; Zhang et al. 2024, A&A 690, A267.

**Forward note (GH5_tsz_desi_centrals):** the "deeper measurement" this README called for was partly on disk: 206k DESI centrals
on the same map find no tSZ detection and A(k=3) = −0.07 ± 0.39, so the lean did not grow. GH5's null test also shows the
Δχ² rule used here is not a detection test, and that jackknife errors run about 1.4× low.
