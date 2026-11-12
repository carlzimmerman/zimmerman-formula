# EUC5R (BLIND RE-GRADE OF EUC5): RESULT_BLIND

2026-11-12. READING bef8d940d8 (alone, before any script); code and runs f7db373fa1; AMENDMENT F1S 871ab16058
(alone, post hoc, before it ran); F1S run 10312399b2. Written before any EUC5 file other than its FROZEN_CRITERIA.md
and AMENDMENT_A1.md has been opened. κ = ½ FITTED; not theory closed. No outcome here favours the framework.

## Words

| Route | Canonical (9.3603e-11) | Alt (1.132e-10) |
|---|---|---|
| Frozen (SDSS/BOSS `veldisp`) | not re-graded (no SDSS rows on disk outside EUC5; A1 text records N = 7 < 30 → NOT EVALUABLE) | same |
| **A1 (DESI fits), as frozen** | **NOT EVALUABLE** (F1 fails) | **NOT EVALUABLE** (F1 fails) |
| would-be word on the A1 numbers | NO VERDICT (stable over β ±0.2 and seeing 0.9/1.1/1.3″) | NO VERDICT (same) |
| post hoc, "under A1, F1S" | NO VERDICT | NO VERDICT |
| READING R (my declared addition) | NO VERDICT | NO VERDICT |

F2 (DESI against SDSS pipeline) could not be run blind; every word above other than NOT EVALUABLE is conditional on
F2 passing or having fewer than 5 pairs.

## Gates and checks

- J1 Plummer 2.4e-4 (pass), J2 power law with β = 0.3 1.1e-4 (pass), J3 SLACS median σ_pred/σ_meas **0.966** (target
  0.977 ± 0.05, pass, N = 72), J4 median b_dyn − b_lens(true z_s) = **+0.033 dex**. Own checks: point-mass projection
  1e-11, PSF aperture at centre 2e-15, kernel against brute-force aperture 4.9e-5, Salpeter-mass sanity 0.881
  (band 0.85-1.00).
- **F1 FAILS.** Reference: the median-S/N flagged primary (3.51 per pixel, 255 spectra), mock at z = 0.45, 40 noise
  draws: median recovered / input = **0.959, 0.891, 0.835** at 150, 250, 350 km/s (limit ±5 %). Scatter 43, 101, 198
  km/s; only 5, 4, 0 of 40 pass A1.3.
- Why (found after the fail, AMENDMENT F1S): the reference spectrum is at z = 0.745; in the observed window used for
  z = 0.45 its S/N is 1.46 per pixel, so the frozen construction made the mock 2.4× noisier than the reference and than
  the graded spectra (median 3.58, quartiles 2.84-4.21). **F1S** (noise scaled to S/N 3.51, nothing else changed):
  0.972, 0.963, 1.004, scatter 25, 38, 93 km/s, 40/40, 40/40, 37/40 pass A1.3 → passes. Post-gate diagnostic at 10×
  S/N: 1.016, 1.005, 0.997. The fitter is not broken; at the graded S/N it reads 3-4 % low at 150-250 km/s in mocks
  (about −0.03 dex in b if real). The literal mock (template broadened by σ_in only) and a template-mismatch mock
  (5 Gyr, Z = −0.35) were reported only and are noisy at the F1 S/N.
- F3 repeats (primary / secondary): L006604 255 ± 18 / 215 ± 33; L011912 231 ± 21 / 205 ± 30; L012642 262 ± 21 /
  225 ± 38. Within 1.1 σ each; all three secondaries lower.
- MUTATE newton (a₀ → 1e-30): b_med on P +0.202 → +0.225 (canonical), +0.197 → +0.225 (alt); rises; exit 1.

## Sample

A1.1 spectra of S lenses: 73 spectra of 70 lenses (72 flagged, 1 extension); 40 lenses in P. Passing A1.3:
**P 35, S 60** (P drops 5: σ > 500, error > 25 % or |V| > 300). No lens at a search end. One graded P lens lies
outside photo-z 70 % ± 0.1 (dropping it: +0.203). Graded P medians: z 0.43, log M★ 11.58 (rescaled to spec-z),
n 6.1, θ_E 1.10″, σ 268 km/s.

## b_dyn (law S, β = 0, fibre 0.75″, seeing 1.1″; 95 % bootstrap, 2,000, seed 20261112)

| | canonical | alt |
|---|---|---|
| **P (N = 35)** | **+0.202 [+0.117, +0.267]** | **+0.197 [+0.112, +0.261]** |
| S (N = 60) | +0.197 [+0.117, +0.267] | +0.192 [+0.112, +0.258] |
| P, β −0.2 / +0.2 | +0.213 / +0.188 | +0.209 / +0.183 |
| P, seeing 0.9 / 1.3″ | +0.196 / +0.209 | +0.192 / +0.204 |
| P, law B | +0.213 [+0.132, +0.281] | +0.210 [+0.128, +0.277] |
| P, θ_E < 1.0″ (N = 13) | +0.116 [−0.016, +0.294] | +0.109 [−0.022, +0.290] |
| P, 1.0-1.3″ (N = 10) | +0.176 [−0.002, +0.335] | +0.171 [−0.006, +0.333] |
| P, > 1.3″ (N = 12) | +0.259 [+0.167, +0.289] | +0.253 [+0.160, +0.284] |
| P, 1.3-1.7″ / > 1.7″ (N = 7 / 5) | +0.252 / +0.267 | +0.245 / +0.261 |
| S, < 1.0 / 1.0-1.3 / > 1.3″ (N = 19 / 16 / 25) | +0.002 / +0.205 / +0.252 | −0.005 / +0.201 / +0.245 |

Every interval has its upper bound above 0.15 and its lower bound below 0.25: the would-be word is NO VERDICT. b_dyn
rises with Einstein radius, as EUC1's lensing map did.

Reported, no word (P, law S): `b_dyn − b∞` median **+0.116** (canonical) / **+0.132** (alt); fraction below −0.25
0.057 / 0.029; b∞ median +0.023 / −0.004. CONDITIONAL on one potential and on the model: source redshift at which the
lensing boost equals the dynamical boost, median 1.76 / 1.65 over the 69 % of lenses with a solution; 31 % have
b_dyn < b∞ (no solution).

## Real-spectra scale (declared in READING §4)

My fitter on the 30 SLACS SDSS spectra against the published SLACS σ: degraded to DESI noise (S/N 4.81 per rest Å)
**s = 1.057 [0.989, 1.103]**, per-lens scatter 0.17; as observed s = 1.049 [1.014, 1.108]. My fits read about 5 % above
Bolton's. READING R (DESI σ / s, envelope of s's bounds): P **+0.151 [+0.027, +0.277]** canonical, **+0.146
[+0.021, +0.271]** alt → would-be NO VERDICT. The interval on s contains 1 at DESI noise, so READING R is consistent
with no scale; it lowers b_med by 0.05 dex and widens the interval.

## Caveats, unverified

- F2 not run: no SDSS dispersion of an ECLIPSE lens was available to me.
- DESI and SDSS wavelengths are vacuum, E-MILES is air: fitted V carries about +80 km/s. Not corrected (A1 does not
  ask for it); its effect on σ is not measured here.
- The fitted error is propagated through the resolution correction (err_fit · σ_fit/σ); using err_fit unpropagated
  changes the quality status of 2 lenses. Not run as a reading.
- No arc-light dilution, no aperture or radial-gradient correction beyond the Jeans model, catalogue n and R_e taken
  as given (n up to 10).
