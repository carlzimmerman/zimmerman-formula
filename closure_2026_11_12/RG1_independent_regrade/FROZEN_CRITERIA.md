# RG1 FROZEN CRITERIA: independent re-implementation of NMB1, PLT1, MWJ1, MWG1, MWI1

Written 2026-11-12, before any script of this lane and before any number of this lane was formed.
Regrade lane. Adopts nothing. Relabels nothing by itself. kappa = 1/2 FITTED; not theory closed.

## Question

Five lanes (NMB1, PLT1, MWJ1, MWG1, MWI1) were written and graded today by one author. Does an
independent implementation, built from their FROZEN_CRITERIA.md files alone, land on the same
headline numbers?

## Blind rule (what this lane may and may not read before its own numbers are saved)

May read: the five lanes' FROZEN_CRITERIA.md (no AMENDMENT files exist for them at freeze time);
closure_2026_11_11/DW1_desi_dr2_mw_mass/dw1.py (McMillan 2017 baryon model and constants);
deepseek_push/G239_proper_efe/g239.py (external-field angle average); the downloaded figure data.

May NOT read until this lane's numbers are saved in this folder: nmb1.py, plt1.py, mwj1.py,
mwg1.py, mwi1.py, plt1_posthoc.py, any .out or .json file in the five lane folders, and their
RESULT.md files. After the numbers are saved: read their outputs and RESULT.md, compare, and for
any difference read their scripts and find the cause.

## Input

Zenodo record 23712180, desi-dr2-mw-mass-figdata.zip, 2,652,537 bytes,
md5 5b0cc3aa9947286eb9348e947d01182d (verified on download, kept outside the repository).
Files used: fig10/desi-dr2-menc.csv, figA1/*.csv, figA2/*.csv, fig08/summary.csv, fig13/*.csv.

## Implementation choices fixed now (where the lanes' criteria leave room)

Constants as DW1: G = 6.674e-11, Msun = 1.989e30 kg, kpc = 3.0857e19 m. Kernel
nu(y) = 1/(1 - exp(-sqrt(y))). Angle average done with 400-point Gauss-Legendre in mu (my choice;
G239 uses a 4001-point trapezoid). McMillan 2017 baryons re-typed from DW1 (component parameters
only); spherical enclosed mass computed by my own quadrature (disc surface density times vertical
CDF at height sqrt(r^2 - R^2), Hernquist bulge).

NMB1:
- N1. RRL mocks (figA1) and BHB mocks (figA2) are paired by (halo, view) to form cross-tracer
  covariance. (The NMB1 criteria say "eight residual series" over "24 mocks", implying the pairing,
  but do not state it.)
- N2. M_true at 30 and 80 kpc: linear interpolation of truths.csv in (log r, log M) per halo.
  Mock estimates at 30 and 80 are on their grids (interpolated the same way if not).
- N3. Error calibration K: at each radius, S built from the mock residuals of all curves at that
  radius only (six at 30, eight at 80), same lambda = 0.5, same C = C_stat + S_res, combined error
  sigma_mine = (1^T C^-1 1)^(-1/2), k_r = max(1, published/sigma_mine). KA4 uses the same.
- N4. Line: M_sph from my own port of McMillan (the criteria's fractions 0.9777 / 0.9972 times
  6.681e10 are checked against it; graded numbers use the port).
- N5. Correlation of theta: V_12/sqrt(V_11 V_22).
PLT1:
- P1. Rows selected r_kpc >= 100 (100 included). Line evaluated at each row's own r.
- P2. Median of an even number of pulls = mean of the two middle values.
- P3. If the line equals the row exactly, sigma_lo is used (no effect expected).
MWJ1 / MWG1:
- J1. G1 uses my own NMB1 theta and V (not the lane's), so G1 differences propagate from NMB1.
- J2. A grid e_N in [0, 0.03] step 0.0005 (61 values), A in [0.70, 1.80] step 0.01. The field
  range at A = 1 is reported as the min and max passing e_N, and contiguity is checked.
- G1h. Hot gas M_hot(<r) = M_ref (r/r_ref)^p is added to the census at every radius (30 and 80 kpc
  for G1 and every row radius for G2/G2p), with no cap beyond r_ref, as written. A capped variant
  (M_hot constant beyond r_ref) is reported, not graded.
MWI1:
- I1. Hot gas 0.15 x 10^10 exactly as written in the criteria (the MB15 value at 27 kpc, 0.1526,
  is reported as a variant). The geometry block (scale-length force ratios) is not re-implemented.

## Targets and tolerances for "reproduced"

| lane | quantity | target | tolerance |
|---|---|---|---|
| NMB1 | theta_30, theta_80 (log10 Msun) | 11.4059, 11.8047 | 0.003 dex each |
| NMB1 | sigma_30, sigma_80 | 0.0270, 0.0567 | 10 per cent each |
| NMB1 | correlation | +0.183 | 0.05 |
| NMB1 | Q: E1 can, E1 alt, E0 can, E0 alt | 4.89, 2.91, 2.40, 0.05 | 0.3 each |
| PLT1 | class medians r >= 100: E1 can H, S; E0 can H, S | -0.68, -1.56; +1.01, +0.28 | 0.05 each |
| PLT1 | S median r >= 150 under E1 canonical | -2.72 | 0.05 |
| MWJ1 | field range at A = 1 passing G1, G2, G2p | 0 to 0.0075 both footings | one grid step (0.0005) |
| MWG1 | field range with MB15 gas, canonical | 0 to 0.0195 | one grid step |
| MWG1 | S plateau median at e_N = 0.01273 with MB15 gas (canonical) | -1.34 | 0.05 |
| MWI1 | required stellar mass, 1e10 Msun | 7.05-7.41 can, 6.36-6.73 alt | 0.02 each |
| MWI1 | z canonical: LN15, McM17, C20, I25, L25 | +0.85, +2.84, +4.68, +4.14, +12.24 | 0.05 each |

Line checks (instrument, before comparing): E0 at 80 kpc 5.691 / 6.219, E1 (0.01273) at 80 kpc
4.977 / 5.109 x 10^11, each within 0.5 per cent; census total 6.681e10 within 0.1 per cent.

Where the target is given only for one footing, the other footing is computed and reported.

## Labels per lane

- **REPRODUCED**: every target number within tolerance.
- **REPRODUCED WITH DIFFERENCES**: every graded label of the lane unchanged, but at least one number
  outside tolerance; each difference listed with its cause.
- **NOT REPRODUCED**: a number outside tolerance that changes a graded label of the lane (a gate
  PASS/FAIL, a window edge that moves the label, a class), stated with the cause.
- Any place where a lane's frozen criteria admit two readings that give different numbers is
  reported as an AMBIGUITY finding, whatever the label.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
