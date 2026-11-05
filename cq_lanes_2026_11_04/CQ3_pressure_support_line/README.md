# CQ3_pressure_support_line: NOT ONE LINE on both footings. The four dispersion-support excesses do not fall on E = k P of one pressure variable: canonical k 0.214 +- 0.011 with chi2 1039 / 9, alt k 0.191 +- 0.012 with chi2 960 / 9, every sample's own k breaks from the joint k by 3.4 to 19 sigma, and no pair or triple of samples passes. By the lane's rule the idea is dropped

Criteria: `FROZEN_CRITERIA.md` (963bc31242) and `AMENDMENT_A1.md` (33ec245b34), each committed alone before the script was ever run. `cq3_line.py`, `cq3_line.out`, `cq3_line.json`, `cq3_line_MUTATE.out`, `cq3_line_MUTATE.json`. **Not blind**: the four excesses were on record. κ = ½ FITTED and held fixed; not theory closed. Footings (canonical a0 9.3603e-11, alt 1.1312e-10) are never pooled. No particle, no cold sector, no new field, no download. Nothing here says the data favour the framework. A description, not an action. 3.5 s, one thread, 144 MB.

**Question.** Do the record's four excesses (VS1 slow rotators, HX1 MaNGA ellipticals, KU1/KU2 early types, CW6 red lenses) lie on one line E = k P, E = log10(M_needed / M_law), with P = σ²/(σ² + V²) at the effective radius and one k per footing?

## Result
| | canonical | alt |
|---|---|---|
| joint k, dex per unit P | 0.2138 +- 0.0114 | 0.1911 +- 0.0116 |
| chi2 / dof, p | 1039.3 / 9, 6e-218 | 960.2 / 9, 7e-201 |
| S1 VS1 own k, z against joint | +0.143 +- 0.014, -5.15 | +0.130 +- 0.014, -4.36 |
| S2 HX1 | +0.558 +- 0.034, +9.98 | +0.539 +- 0.034, +10.14 |
| S3 KU | +1.908 +- 0.089, +18.95 | +1.725 +- 0.090, +17.10 |
| S4 CW6 | +0.123 +- 0.027, -3.40 | +0.066 +- 0.027, -4.70 |
| **Label** | **NOT ONE LINE** | **NOT ONE LINE** |

The ten points, canonical (alt in `cq3_line.out`; the alt E are lower by 0.01 to 0.04 dex at every point, same P):

| Sample | Point | n | P | E, dex | stat | shared sys |
|---|---|---|---|---|---|---|
| S1 VS1 | slow rotators | 4 | 0.998 | +0.182 | 0.017 | |
| S1 VS1 | fast rotators | 12 | 0.897 | +0.062 | 0.021 | |
| S2 HX1 | MaNGA Q1 (σ low) | 305 | 0.624 | +0.143 | 0.011 | 0.072 |
| S2 HX1 | Q2 | 304 | 0.683 | +0.249 | 0.009 | 0.077 |
| S2 HX1 | Q3 | 304 | 0.835 | +0.306 | 0.011 | 0.074 |
| S2 HX1 | Q4 | 305 | 0.909 | +0.361 | 0.008 | 0.072 |
| S3 KU | slow | 536 | 0.994 | +0.619 | 0.008 | 0.106 |
| S3 KU | fast | 5520 | 0.619 | +0.517 | 0.002 | 0.063 |
| S4 CW6 | red lenses | 3840 | 0.720 | +0.118 | 0.021 | |
| S4 CW6 | blue lenses | 2216 | 0.536 | -0.056 | 0.036 | |

n: S1 the lane's own galaxies; S2 the Tian galaxies in the rung (the DynPop count behind each rung's P is in `cq3_line.json`, n_dyn); S3 the DynPop classes; S4 the DynPop galaxies behind P, not the lens counts. P comes from λ_Re through Emsellem et al. 2007's λ_R–V/σ relation (κ_E 1.1), averaged over the members.

## What it reads
- **Same P, very different E.** At P between 0.90 and 1.00: VS1 fast +0.06, VS1 slow +0.18, HX1 Q4 +0.36, KU slow +0.62. P is bounded by 1, so a sample at +0.6 needs k of at least 0.6 while VS1's fast rotators at +0.06 need k P_fast of 0.06; one k cannot serve both without a P below 0.1 for the fast rotators, which the map does not give. The spread among estimators and surveys at the same P is larger than any P effect.
- **No subset rescues it** (beside): without S3, chi2 202 / 7 (canonical); without S2, 886 / 5; S1 and S4 alone, the best pair, 29 / 3 (p 2e-6); every pair fails (S1+S2 182 / 5, S1+S3 868 / 3, S2+S3 713 / 5, S2+S4 154 / 5, S3+S4 852 / 3), so every triple fails too (the samples' chi2 add at one k, so a triple's chi2 can only exceed any pair inside it). Alt reads the same.
- **CW6's blue lenses sit below the law** (-0.056 +- 0.036 canonical, -0.096 alt), where a positive k wants them above it. S1's and S4's own k agree with each other (0.143 +- 0.014 and 0.123 +- 0.027 canonical) but not with the joint k, and their two points each are not on a line through the origin (E / P +0.18 and +0.07 for VS1, +0.16 and -0.10 for CW6).
- **A line with an intercept fails as well**: E = E0 + k P gives E0 +0.27, k -0.08, p 1e-116 (canonical).
- **The absolute-level caveat does not carry it.** Reading the NSA masses as h = 0.7 (+0.31 dex, LAM9) takes S3 to +0.39 / +0.30 and the fit to chi2 367 / 9 (alt 326 / 9): still NOT ONE LINE. P = 1 - λ_Re in place of the Emsellem map fails too (chi2 1350 / 9).
- **The P -> 0 end is fine and says little**: SPARC discs +0.012 +- 0.016 (canonical, z +0.69 against the line at P 0.003) and -0.018 +- 0.016 (alt, z -1.10).
- **Post-hoc and calibration-free, not graded** (h). Slope dE/dP inside each sample with a free intercept, canonical (alt within 0.04): S1 +1.19 +- 0.27, S2 +0.65 +- 0.04, S3 +0.27 +- 0.12 as classed (+0.05 +- 0.04 at matched M* and σ_Re from KU2's D over a matched ΔP of 0.223), S4 +0.95 +- 0.23; common slope +0.39 +- 0.03, chi2 117 / 3. So even with every absolute level removed, VS1 and CW6's colour split agree at about +1 dex per unit P, HX1's rungs rise at +0.65, and KU2's matched test is flat, 4 sigma below VS1: the old KU2-against-VS1 split, now in P.

## Checks
- **K1 PASS**, both footings, before the label: VS1 group means (|d| <= 1.2e-4), HX1 rung median B_need (exact, four rungs), KU1 class median residuals (<= 2e-16), CW6 A against the CW6 README (<= 4.6e-4).
- **K2 PASS**: a planted E = 0.2 P with noise from the real covariance reads ONE LINE in 0.865 (canonical) / 0.864 (alt) of 2000 draws (need 0.70); with P shuffled, 0.001 / 0.002 (need <= 0.10). The pipeline can return ONE LINE.
- **MUTATE twin** (P shuffled across the ten points, seed 20261104): NOT ONE LINE on both footings, exit 1 by design. On the real E, 0 of 2000 shuffles read ONE LINE.

## Expectations on record against results
| Expectation (criteria) | Result |
|---|---|
| NOT ONE LINE both footings, 75 % | Right |
| NOT EVALUABLE, 15 % | No: k / sigma_k is 16 to 19 |
| ONE LINE, 10 % | No |
| Expected breaker: S3 | S3 is the largest (z +17 to +19), but all four samples break |
| Slow and fast P differ by only about 0.1 | Right: VS1 0.998 against 0.897 |

## Disclosures
1. **AMENDMENT A1** (before any run): the 30-member floor applies to the DynPop population that gives a point its P, not to VS1's own 4 and 12 rotators; the working population is KU1's selection restricted to finite residuals (6056 of 6056).
2. **Beside row (c) had the wrong sign in the criteria.** They wrote "log M lowered by 0.31 dex"; LAM9 says the h = 0.7 reading adds 0.31 dex and lowers r by about 0.5 ln. The first run used the wrong sign (S3 E rose to +0.83 / +0.72). Corrected before any output was committed. No graded number changed.
3. **Rows (g) and (h) were added after the first read** of the graded result. They are labelled post-hoc and change no label. (h) takes KU2's committed D and sigma_D and a matched ΔP computed here with KU1's cell definition.
4. **The Emsellem constant is quoted, not re-read** (no download).
5. **Two surveys' λ_Re are used without a verified common zero point**: ATLAS3D's for VS1 and MaNGA DynPop's for S2 to S4 (DynPop's red P is 0.72 against VS1's fast ellipticals at 0.90). Only the 1 - λ variant was tried; a remapping was not, and would be a free knob.
6. **HX1's E is larger than the README's "law close to Newton" suggests**: log10(σ_O² / σ_L²) of +0.14 to +0.36 dex. The B_need reproduction is exact; the conversion is the criteria's.
7. **S2's own k carries a small error (0.034)** because its 0.07 dex shared mass systematic is fully correlated across rungs and cancels in the slope. S2 and S3 are the same survey with different estimators, so they are not independent.

## Caveats kept as caveats
KU's absolute level is uncalibrated (NSA h convention, kcorrect masses, sphere-enclosed JAM mass; beside row (c) moves it, the label stays). HX1's need is model-dependent (an IMF would also raise it). The colour map is a population map, MaNGA galaxies standing in for KiDS lenses, and the lensing amplitude is halo-scale while P is half-light. P is taken as exact. VS1's errors are scatter only.

## Run
```
cd cq_lanes_2026_11_04/CQ3_pressure_support_line
export OMP_NUM_THREADS=1 PYTHONHASHSEED=0
nice -n 10 python3 -I cq3_line.py            # exit 0
nice -n 10 python3 -I cq3_line.py --mutate   # exit 1 by design
```
HX1's own text (lines 1-37 of its script, the output-file line swapped for a null file) is executed for the Tian rungs; no file outside this folder is edited.
