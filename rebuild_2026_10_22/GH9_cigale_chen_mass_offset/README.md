# GH9_cigale_chen_mass_offset

**Question.** GH8's class, BELOW ROUTE E'S NEED, was limited by the stellar-mass scale: its lenses use DESI CIGALE masses, while Zhang+24's gas normalisation sits on SDSS masses from Chen+12. How far apart are they, and does the class survive?

**Verdict: SURVIVES MASS SCALE.** CIGALE runs about **0.19 dex below** the Chen-method table, the opposite of the feared direction. BELOW holds at D1, D2 and D3 at all three R. The mass scale is no longer GH8's main limit.

| Offset graded | Δ_j by lm cell | A(1) | A(1.8) | A(3) | A(1.8) + 2σ |
|---|---|---|---|---|---|
| none (GH8) | 0 | 0.55 ± 0.35 | 0.26 ± 0.20 | 0.23 ± 0.17 | 0.67 |
| **D1** primary | −0.237, −0.208, −0.174, −0.150 | 0.39 ± 0.27 | **0.24 ± 0.19** | 0.30 ± 0.19 | 0.61 |
| D2 same IMF (+0.04) | D1 + 0.04 | 0.42 ± 0.28 | 0.24 ± 0.19 | 0.27 ± 0.18 | 0.61 |
| D3 to lens z (−0.037) | D1 − 0.037 | 0.37 ± 0.26 | 0.24 ± 0.19 | 0.33 ± 0.20 | 0.62 |

(R_fm, shuffle σ. R_cut and R_ctx give A(1.8) + 2σ of 0.59–0.64.)

## What it shows

- **Offset:** 36,596 pairs at z 0.1–0.19, median −0.188, MAD 0.125. It is mass dependent (−0.24 to −0.15) and differs by type: passive −0.14, star-forming −0.31. North −0.189, south −0.183.
- **A(1.8) barely moves** (0.26 → 0.24). A higher mass raises M_hot but also R_vir, which spreads the gas over more sky and out of the compensated aperture, so the two nearly cancel at k = 1.8.
- **Break-even corrects GH8.** With the model properly rebuilt, CIGALE would have to be about **+0.27 dex high** (+0.26 at R_ctx) to remove the class. GH8's README said 0.2 dex and "0.41 ± 0.30"; that was a linear rescaling that ignored R_vir. The rebuilt value at +0.2 is 0.36 ± 0.26, A + 2σ 0.88. The measured offset is about 0.46 dex from break-even.
- **Normalisation lock now applies.** At D1, A(1) + 2σ is 0.91–0.96 at all R, so the frozen wording is "below Zhang-normalised gas at every extent". The shortfall then concerns the X-ray normalisation or the column, **not extension past R_vir**. This is narrow: at D2 with R_ctx, A(1) + 2σ reaches 1.01.

## Is this table on Zhang's scale? (post-hoc, not frozen)

Zhang's paper cites Chen+12 but does not name this table, so I compared sky densities in the MGS-targeted Wisconsin rows with Zhang's FULL_spec counts on 4010 deg² (`gh9_counts.py`, Wisconsin area 8169 deg² by a pixel cut I chose).

| Shift added to Wisconsin | 10.5–11 | 11–11.25 | 11.25–11.5 |
|---|---|---|---|
| −0.20 (about CIGALE's scale) | 0.91 | 0.58 | 0.39 |
| −0.05 | 1.15 | 1.05 | 0.99 |
| **0** | **1.21** | **1.23** | **1.25** |
| +0.05 | 1.26 | 1.39 | 1.53 |

The ratio is flat only near zero shift, and flatness does not depend on the area. That supports the table being on Zhang's scale within a few 0.01 dex, and rules out Zhang's masses being on CIGALE's scale. **Not explained:** the common 1.2× excess (area, masks or sample cuts are possible), and the 10–10.5 bin, which gives 1.33. This check was designed after seeing Δ.

## Limits

1. **Lenses leave Zhang's bin.** On this scale, GH8's lenses are about log M★ 10.8–11.15, while the 1.84 M★ normalisation comes from Zhang's 10.5–11 bin (median 10.74). The model extrapolates that ratio, and the frozen rule did not re-select lenses. A sample truly on Zhang's bin was not stacked.
2. **Overlap ≠ lenses.** Pairs are 21 % of the DESI parent at 0.1–0.19, biased to bright galaxies, and stop at z 0.19, against a lens median of 0.26. The in-overlap slope is −0.95 per unit z, and steep only in the last bin, likely selection; the GKV bridge gives −0.037 and the slope −0.12. Both make Δ more negative, and a Δ change this size leaves the class alone.
3. **One offset per mass cell** mixes passive and star-forming lenses, which differ by 0.17 dex.
4. **GH8's other limits are untouched:** marginal control after post-result fixes, inherited β, K2 failure, not blind, no detection (null p 0.21), extent not measured.
5. **Memory:** the matching step peaked at 13.3 GB against the frozen 6 GB limit, while X48 zooms ran. They were still running afterwards. Propagation peaked at 0.7 GB.
6. **Proxy IMF:** Kroupa is from the SDSS data model; Zhang's IMF is not stated in the text I read.

**For the theory.** The kSZ column remains below what route E needs, now without the mass-scale escape, and also comes out low at R_vir on the corrected scale. That hints at normalisation or pipeline rather than extent, and doesn't say gas is excluded or that the law wins. Route E's lensing gap remains unsolved. κ = ½ FITTED; c_f EXTERNAL; cold dark energy is a gravitating field component, never a particle; not theory closed; nothing here says the data favour the framework.

## Checks

All PASS: K1 match (median |Δz| 5e-5, 0.07″); K2a model rebuild exact; K2b GH8 A(1.8) reproduced 0.2625; K3 injection; K4 (≥ 8679 pairs per cell); K5 bridge; MUTATE MAD ×1.55, v flip exact. The break-even interpolation had a bug in the first run (it returned 0.3) and was fixed; grades unchanged.

## Files

`FROZEN_CRITERIA.md` (2c54296d9c), `gh9_match.py`, `gh9_prop.py`, `gh9_counts.py` with `.out` and `.json`. Run in that order after GH8, `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15`. Data: `_external_data/sdss_wisconsin_pca/` (143 MB, whole table, FETCH_LOG with sha256; published checksum not checked).

**Sources:** SDSS Wisconsin PCA (https://www.sdss4.org/dr17/spectro/galaxy_wisconsin/); Chen et al. 2012, MNRAS 421, 314; Zhang et al. 2024, A&A 690, A267; DESI DR1 CIGALE VAC; Driver et al. 2022 (GKV).
