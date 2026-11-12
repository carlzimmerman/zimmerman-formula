# NMB1 RESULT: the framework's zero-parameter line against the shape-measuring curves of DESI DR2 Results III

2026-11-12. Criteria: `FROZEN_CRITERIA.md`, committed alone (1fd8ca964e) before the script existed
and before any per-method real-galaxy value was read. TEST lane. Adopts nothing. Relabels no other
lane. kappa = 1/2 FITTED; not theory closed.

## Labels

| case | line at 30 / 80 kpc [10^11 Msun] | Q (gate 6.180) | z_30 | z_80 | slope pull | label |
|---|---|---|---|---|---|---|
| E1 canonical | 2.326 / 4.977 | 4.89 | -1.46 | -1.90 | -1.18 | **PASSES, FRAGILE** |
| E1 alt | 2.517 / 5.109 | 2.91 | -0.19 | -1.70 | -1.57 | **PASSES** |
| E0 canonical | 2.331 / 5.691 | 2.40 | -1.42 | -0.87 | -0.19 | **PASSES** |
| E0 alt | 2.526 / 6.219 | 0.05 | -0.13 | -0.19 | -0.13 | **PASSES** |

E1 is the record's operative reading since G239 (QUMOND angle average in the Local Group field,
e_N = 0.01273); E0 is the no-field limit. Negative z means the line is below the data.

E1 canonical is FRAGILE because two of the six pre-named variants put it on the other side of the
gate: lambda = 1 (Q = 6.90) and no error calibration (Q = 7.88). The other three cases pass under
every variant.

**The gate has little power.** It rejects a line with the baryons doubled or halved (Q = 28 to 65)
and a point mass (Q = 226), but it cannot tell the framework from the paper's own NFW (Q = 0.17),
nor E0 from E1. A pass here means "not excluded by the only shape-measuring curves", and no more.

## The instrument, as it came out

| curve | 30 kpc | 80 kpc |
|---|---|---|
| NIMBLE-A RRL | 2.449 (2.334, 2.595) | 6.678 (6.030, 7.403) |
| NIMBLE-A BHB | 2.481 (2.370, 2.618) | 5.993 (5.112, 6.943) |
| NIMBLE-B RRL | 2.787 (2.589, 3.004) | 6.181 (5.525, 7.244) |
| NIMBLE-B BHB | 2.569 (2.374, 2.785) | 6.543 (5.752, 7.430) |

Median and 16th to 84th percentiles, 10^11 Msun. With the covariance of the paper's 24 mocks
(shrinkage 0.5) and the error calibration (k_30 = 1.000, k_80 = 1.392):

- NIMBLE-only mass at 30 kpc: 2.546 x 10^11, log10 = 11.406 +/- 0.027 (6 per cent).
- NIMBLE-only mass at 80 kpc: 6.379 x 10^11, log10 = 11.805 +/- 0.057 (14 per cent).
- Correlation between the two: +0.18. Slope d ln M / d ln r from 30 to 80 kpc: 0.936 +/- 0.137.
- The eight numbers agree with each other far better than the covariance requires (chi-square 1.51
  on 6 degrees of freedom, p = 0.96). The mock-calibrated errors are generous for these curves.

For comparison, Table 4's joint has 11.423 +/- 0.022 and 11.804 +/- 0.035. At 30 kpc the
shape-measuring curves sit 4 per cent below the joint; emPDF pulled the joint up there.

## What this says

1. **Shape.** The measured 30 to 80 kpc slope is 0.94 +/- 0.14. The line has 0.91 to 0.92 with no
   field and 0.72 to 0.78 with the field; the paper's NFW has 0.93. All are inside 1.6 sigma. The
   release does not measure the shape well enough to separate any of them.
2. **Amplitude, no field.** Against the shape-measuring curves the canonical line is 1.4 sigma low
   at 30 kpc and 0.9 sigma low at 80 kpc. DR2REV's post hoc reading against the joint (2.3 to 3.5
   sigma low at 20 to 65 kpc, diagonal errors) shrinks to this once the imposed-shape methods are
   removed and the mock covariance is used.
3. **Amplitude, with the field.** The line is 1.9 (canonical) and 1.7 (alt) sigma low at 80 kpc.
   Inside the gate, and canonical only just.
4. **The baryon amplitude that would centre the line** (reported, not graded): 1.17 [1.06, 1.30]
   canonical and 1.02 [0.92, 1.13] alt with no field; 1.21 [1.10, 1.33] and 1.09 [1.00, 1.20] with
   the field. A = 1 is outside the one-sigma interval on the canonical footing in both readings.
   DW1's 1.33 +/- 0.04 from the joint table is not reproduced: the shape-measuring curves ask for
   about half that excess, with three times the error.

## Reported, not graded

- **Published bands taken at face value** (no mock covariance): Q = 24.2 (E1 canonical), 13.2 (E1
  alt), 11.05 (E0 canonical), 0.26 (E0 alt). Every pass above except E0 alt depends on the
  mock-calibrated covariance. The paper itself says its methods' reported errors are too small,
  which is why the calibrated covariance was the graded one.
- **Matched-field AQUAL values of today's correction lane** (4.487 / 4.579 x 10^11 at 80 kpc, point
  mass, a different kernel): pulls -2.70 / -2.54 at 80 kpc. Since Q can never be smaller than the
  square of either single-radius pull, that reading would fail this gate (Q >= 7.3 / 6.5) whatever
  its 30 kpc value. Not graded, because the record has no 30 kpc value for it.
- **The paper's NFW** (1.19 x 10^12, c = 12): 2.485 / 6.205, Q = 0.17, passes.
- **The imposed-shape methods at 80 kpc:** emPDF 6.08 (+2.45, -0.86) RRL and 6.68 (+2.08, -1.13)
  BHB; GME 5.29 (+0.45, -0.49) RRL and 6.36 (+0.49, -0.51) BHB.

## Checks

KA1 to KA6 pass (file hash; fig10's joint rows match Table 4 to 0.005; mock residuals reproduce
Figure 8 to 0.01 point; the machinery on all curves gives 11.419 at 30 kpc and 11.788 at 80 kpc
against Table 4's 11.423 and 11.804; closed form to 1e-16, synthetic mean Q 2.001 and rejection
rate 0.0466; the line reproduces the record at 80 kpc to 0.01 per cent). M1, M2 and M3 bite
(`nmb1_mut.out`). A hand recomputation of Q from the printed theta, errors and correlation gives
2.405 (E0 canonical) and 4.878 (E1 canonical) against the script's 2.40 and 4.89.

## Disclosures

- **Run 1 stopped at KA4** before any graded number was computed (`nmb1_run1_stopped.out`). The
  check compared the file's log10(M / 10^11 Msun) with Table 4's log10(M / Msun), an offset of
  exactly 11. The reference in the check was corrected; the criteria were not touched.
- **One implementation choice the criteria do not fix:** whether the lambda variants recompute the
  error calibration with their own lambda (used) or keep the graded one. Both are printed; no case
  changes side between them.
- The per-method floor of the paper's formalism is unpublished and is replaced by the error
  calibration K, as frozen.

## Limits

- The covariance comes from six LambdaCDM haloes with no LMC, whose true 50 to 80 kpc slopes are all
  0.64 to 0.72. The bias corrections inside the fig10 curves are the paper's and were calibrated on
  the same haloes.
- Two radii only, because the calibration needs mock residuals at matched radii and the gate was
  frozen on 30 and 80 kpc.
- The baryon census is McMillan 2017 at A = 1, spherically reduced as in DW1.
- The NIMBLE paper itself is not out. When it is, the measured dispersion and density profiles
  allow the Jeans mass to be recomputed without the LambdaCDM-calibrated correction.

## Files

`FROZEN_CRITERIA.md`; `nmb1.py` (takes the path of the Zenodo zip as its argument; the zip is not
stored here; md5 5b0cc3aa9947286eb9348e947d01182d); `nmb1.out`; `nmb1_results.json`;
`nmb1_mut.out`; `nmb1_run1_stopped.out`.
