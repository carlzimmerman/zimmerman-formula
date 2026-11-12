# DW1 — DESI DR2 III (arXiv:2611.05518) Milky Way mass vs the framework

Committed BEFORE `dw1.py` and before any number was computed. Nothing below is re-tuned after the run.

## The external result being absorbed

DESI DR2 Results III (submitted ApJ, 3 Nov 2026), 10,036 RR Lyrae + BHB halo stars with 6D phase
space, 10-95 kpc, four dynamical-modeling methods, mock-calibrated, joint estimates:

- `M(r<80 kpc) = 6.36 (+0.53 / -0.48) e11 Msun`  (largest radius directly probed; no M(<r) reported beyond 80 kpc)
- `M200c = 1.19 (+0.14 / -0.12) e12 Msun`
- Table 4: the joint enclosed-mass profile at 13 radii, 20 to 80 kpc in 5 kpc steps, with errors.
  Those 13 points are the test; the M200c number is an extrapolation the paper itself flags as such
  ("we do not report an enclosed mass estimate beyond 80 kpc").

All 13 table rows are transcribed in `dw1.py` from the arXiv HTML text layer; the profile is the
instrument.

## The framework's prediction, stated before the run

No dark-matter particle; the dynamical mass is `M_dyn(<r) = nu(|g_bar(r)|/a0) * M_b(<r)` with
`nu(y) = 1/(1-exp(-sqrt(y)))` (the repo's Route A kernel, `hunt_2026/hunt_lib.py`), `g_bar` the radial
force of the McMillan 2017 baryon model, `M_b(<r)` its spherical enclosed mass, and both registered
footings `a0 = {9.36e-11, 1.13e-10} m/s^2`. Zero fitted parameters. The external field enters only in
the mutation block (the framework's own scalar-additive EFE approximation, `e_N = 0.0127`, the repo's
committed Local-Group vector sum).

`M_b = 6.681e10 Msun` (McMillan 2017 thin+thick+bulge+HI+H2, the repository's validated census).
One amplitude nuisance `A` (`M_b -> A*M_b`) is allowed wherever a SHAPE question is being asked; every
amplitude statement is quoted both with `A = 1` (absolute prediction) and with `A` free.

## Pre-registered checks and pass conditions

| id | question | pass condition |
|----|----------|----------------|
| V0 | does the ported instrument reproduce the repo's committed item-38 anchor? | `M_dyn(73 kpc) = 5.23e11` (canonical) / `5.71e11` (alt), each to <1% |
| V1 | does the McMillan model reproduce its own published component masses? | each component within 2% of `hunt_2026/h34_h35_h38_milky_way.out` |
| V2 | is the Hankel radial force right? | numerical `S(k)` vs the analytic exponential transform <2% for k<20/kpc; total force → `G M_b/r^2` within 1% at 40 kpc |
| V3 | is the spherical reduction honest at the radii tested? | `M_sph(<r)/M_b` reported at every r; no verdict is quoted where the force and the enclosed mass disagree by >10% |
| DW1a | ABSOLUTE amplitude at 80 kpc, both footings | `|M_pred - 6.36e11| <= 2 sigma`, `sigma = 0.50e11` (mean of +0.53/-0.48) |
| DW1b | does the ONE-parameter profile fit the whole 13-point table? | `chi2/13 < 2` with `A` free (diagonal errors; the table's errors are correlated, which this cannot capture — stated, not corrected) |
| DW1c | does the amplitude the profile demands equal the amplitude the framework's OWN outer rotation curve demanded? | `A*(profile)` within 2 sigma of the item-35 range `A = 1.256-1.309` on the McMillan census |
| DW1d | SHAPE: the local log-slope of M(<r) over 60-80 kpc | `|slope_fw - slope_obs| <= 2 sigma_slope`, `sigma_slope = sqrt((s_80/6.36)^2+(s_60/5.19)^2)/ln(80/60)` |
| DW1e | `M200c`: the paper's 1.19e12 vs the framework's EFE-saturated plateau | `|M200c_fw - 1.19e12| <= 2 sigma`, `sigma = 0.13e12`; ALSO the `A` the framework would need to reach 1.19e12 is reported and compared with `A*(profile)` |
| DW1f | FALSIFIER, pre-registered: `M(<150 kpc)` | framework (plateau) and the paper's own NFW(c=12) extrapolation must differ by >20% for the test to be worth registering; the number is the deliverable |

Mutation controls (each must move the relevant statistic the right way, and each is reported as a number,
not an assertion): `a0 x 10`; `nu = 1` (baryons only); the measured profile shuffled between radii;
`e_N = 0.0127` in the scalar-additive EFE.

## What is NOT claimed

- This is not a derivation of the framework's kernel, `a0`, or the baryon census: `A = 1` is
  the prediction, `A` free is a nuisance, and `kappa = 1/2` remains FITTED.
- The paper's mock calibration is ΛCDM-based (AuriDESI); its per-method bias corrections are tuned on
  NFW-like halos, so a non-NFW framework profile may not transfer — a scope limit on the data, recorded,
  not used to excuse a miss.
- `M200c` is not a framework quantity at all. The framework has a plateau, not a virial mass; DW1e
  therefore tests the paper's extrapolation against the framework's saturation value and says so.
