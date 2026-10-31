# GH10_dr2_ksz_published_points

**Question.** Using only the published DESI DR2 × ACT DR6 kSZ points (Hadzhiyska+ 2026, arXiv:2604.19745), is the gas around log M★ 10.5–11 galaxies at the level route E's lensing rescue needs (Zhang's gas to 1.8 R_vir)?

**Verdict: BELOW NEED.** A(1.8) = **0.448 ± 0.105** (A + 2σ 0.66; 0.68 with the paper's 10 % r uncertainty), a detection of the same gas at 4.3σ. This does not rely on my velocity pipeline, and it agrees with GH9's DR1 value (0.24 ± 0.19). **But it does not retire extended gas:** see "The misfit is shape".

| Fit, bin CIGALE 10.5–11 | A(1) | A(1.8) | A(3) |
|---|---|---|---|
| **PRIMARY**, with GH9 offset | 0.59 ± 0.15 | **0.45 ± 0.11** | 0.53 ± 0.11 |
| No mass offset | 0.78 ± 0.19 | 0.47 ± 0.12 | 0.47 ± 0.10 |
| θ ≤ 3′, with offset | 0.66 ± 0.17 | 0.56 ± 0.13 | 0.63 ± 0.13 |
| Bin 10–10.5 (lowest offset extrapolated, no grade) | 0.53 ± 0.27 | 0.39 ± 0.16 | 0.35 ± 0.15 |

χ² after fitting A (13 points): 21.0, 18.7, 14.1 for k = 1, 1.8, 3. Null χ² 37.1. Gas mass, log M★ about 10.97: need M_gas(<1.8 R_vir) ≈ 4.7e11 M☉ (5 M★); measured 2.1e11; A + 2σ limit 3.2e11 (post-hoc, approximate).

## The misfit is shape

| θ (′) | R (Mpc) | T (μK arcmin²) | Model k = 1.8 | (T − m)/σ |
|---|---|---|---|---|
| 1.00 | 0.25 | 0.12 ± 0.03 | 0.17 | −1.7 |
| 1.81 | 0.46 | 0.42 ± 0.12 | 0.84 | −3.6 |
| 2.62 | 0.66 | 1.33 ± 0.31 | 1.54 | −0.7 |
| 3.44 | 0.87 | 2.72 ± 0.73 | 1.90 | +1.1 |
| 4.25 | 1.07 | 4.11 ± 1.39 | 2.00 | +1.5 |
| 6.69 | 1.68 | 9.9 ± 5.6 | 2.02 | +1.4 |
| 10.75 | 2.71 | 27 ± 21 | 2.02 | +1.2 |

- **Inside about 2 R_vir** (1.81′ ≈ 460 kpc ≈ 1.6 R_vir at this mass) the signal is about half of Zhang's gas. The single amplitude is driven by these points; dropping 1′ or 1.81′ gives 0.38 or 0.53.
- **Beyond about 0.9 Mpc** the cumulative signal keeps rising past the model's total. Points are correlated and each about 1–1.6σ, and two-halo signal is unsubtracted.
- **So what fails is Zhang's profile continued to 1.8 R_vir, not extended gas in general.** Route E's fair-share rule depends on baryons to r_ta, so a flatter, more extended gas distribution could still supply the budget. These points can't separate that from two-halo signal. Applying the stop rule now would be premature.

## Limits

1. **My frozen lock overstated "BELOW is conservative".** Satellites and two-halo add signal overall, but miscentring (satellite fraction 0.28 at > 10.5) moves signal out of small apertures, exactly the ones driving A. I did not model it. A correction would raise A by an unmeasured amount; reaching A + 2σ = 1 requires about 1.5×.
2. **Not centrals, not isolated.** The published sample is all galaxies, in halos heavier than MW-mass on average (mean log M_h 13.34, M☉/h, at > 10.5), and each is modelled by its own M★.
3. **Not Zhang's bin.** With the offset, this bin is log M★ about 10.7–11.15; Zhang's 1.84 ratio is from 10.5–11. The 10–10.5 bin covers the lower side and is also low, but with an extrapolated offset and a ratio Zhang does not measure there.
4. **Derived, not published.** The differential bin assumes independent errors and equal v² weighting. The published > 10.5 threshold against this same model gives A(1.8) 0.69 ± 0.09.
5. **Not native.** The points inherit Planck 2018 reconstruction, r_fid 0.64 and σ_true 300 km/s; A scales as 300/σ_true. Model mix uses DR1 z, mean 0.207 in the all-BGS cache against 0.262 in DR2 (M_r cut not applied), so its angular scale is approximate.
6. **K2 is loose.** S/N(> 10.5) is 9.46 from the published covariance against the paper's 8.23, within my 25 % gate, unexplained.
7. **A(1) is low too** (0.59 ± 0.15, A + 2σ 0.89; 0.78 ± 0.19 with no offset, not below). The law's measured-gas input faces the same question, or Zhang's X-ray mass is high.

**For the theory.** Published data, independent of my pipeline, say gas around these galaxies is about half Zhang's profile inside about 2 R_vir. The route E need as GH2 framed it isn't met there, but the rescue isn't closed: the open question is how much gas lies at 1–3 Mpc, separated from two-halo. This doesn't say the law wins. κ = ½ FITTED; c_f EXTERNAL; cold dark energy is a gravitating field component, never a particle; not theory closed; nothing here says the data favour the framework.

## Checks

K1 model vs GH7 within 0.3 %; K2 above; K3 N(> 10.5) 1.54M; K4 C_bin positive definite; K5 injection; MUTATE flip. All PASS. `gh10_post.py` was written after seeing the result and is not frozen.

## Files

`FROZEN_CRITERIA.md` (0e685dc0c8), `gh10.py`, `gh10_post.py`, `.out`, `.json`. Data `_external_data/desi_dr2_ksz_zenodo/` (FETCH_LOG with sha256). Paper values came through a fetch summariser; only Table values quoted above (8.23, f_sat, M_h, r) rely on that.

**Sources:** Hadzhiyska et al. 2026, arXiv:2604.19745, data doi:10.5281/zenodo.19160138; Zhang et al. 2024, A&A 690, A267.
