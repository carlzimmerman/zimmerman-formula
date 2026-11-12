# AZ2R: blind re-grade of AZ2 (flat a0 at z 2.33, DESI DR2 Lya AP pair) - READING (before any script or number)

Criteria re-graded: `closure_2026_11_12/AZ2_flat_a0_lya_ap/FROZEN_CRITERIA.md` (frozen statistic followed; amendments A1/A2 read
as notes on AZ2's own code only). Theory: a0 = (1/2) c sqrt(G rho_DE); tracking a0(z)/a0(0) = sqrt X(z), X = rho_DE(z)/rho_DE(0).
**Blindness disclosure:** AZ2's amendment files (which I was allowed to open) quote AZ2's frozen headline: FLAT HOLDS /
EXPANSION-MODEL DEPENDENT, D_band 1.76 / 1.79, D_rival ~361, free best X5 1.74, mutated headline FLAT FAILS. I have therefore seen
AZ2's outcome before computing. Not opened: AZ2's RESULT.md, script, json/out files.

**Statistic as read.** Flat model E^2 = Om(1+z)^3 + Or(1+z)^4 + (1-Om-Or) X(z), X piecewise-linear on {0,0.4,0.7,1.0,1.5,2.33},
X(0)=1, constant beyond. BAO: BGS D_V/r_d + six anisotropic pairs (2x2 cov each), q = c/(H0 r_d) solved analytically.
SN: Pantheon+ STAT+SYS, non-calibrators, zHD > 0.01, mu = 5 log10[(1+zHEL) D_M(zHD)] + M, M marginalised analytically.
Per cell (T1 BAO, T2 BAO+SN) x (Om 0.25/0.30/0.35) x footing: Delta chi^2_prof(X5) with the other four nodes re-minimised,
relative to the free minimum at that Om. D_band = min over X5 in [0.81, 1.21]; D_rival at X5 = E(2.33)^2 (X = 1, that Om, that Or).
Labels exactly as frozen section 4; headline T2 Om 0.30; EXPANSION-MODEL DEPENDENT flag if Om 0.25 or 0.35 label differs.

**Ambiguities and readings chosen (alternative in brackets).**
1. Profile over X5: continuous - bounded 1-D minimisation (Brent) of the profile inside the band, plus a coarse grid for the
   interval report [a fixed X5 grid only, as AZ2 did; can only raise D_band by the grid step's curvature].
2. Free minimum = lowest of: a multi-start 5-node fit (fixed starts) and every profile evaluation, so Delta chi^2 >= 0
   [free fit alone].
3. X nodes may go negative (as CFG681; E^2 floored at 1e-6 -> chi^2 1e9); sqrt X reported as sqrt(max(X5, 0)) [X >= 0 prior].
4. Footing enters only via Or(h), h = sqrt(rho_DE(0) / ((1-Om) rho_crit,100)) per Om [also via E for the rival point; I use it].
5. KA2 (flat injection) run per footing with that footing's Or [canonical only].
6. Om-profiled row (Om free in [0.15, 0.45]) reported, no label.
7. Distances: my own trapezoid integral on a z grid of step 0.0005 with every node on the grid [CFG681: 5001-point linspace to 2.5].
Taken from CFG681: the data table (DESI DR2 BAO values as typed in `cfg681_bao.py`), the Pantheon+ file location and cuts, the
SN distance convention, h = 0.68 for KA1. Fit code written independently.

**Validation (any failure -> NO VERDICT, grading stops).**
- V1 = KA1 (old Lya pair 38.988 +- 0.531 / 8.632 +- 0.101, r -0.431; h 0.68): T1 Delta chi^2 (X=1 vs free, Om free) 7.41 +- 0.10;
  T2 12.08 +- 0.10; T3 AP chi^2 5.98 +- 0.05; fixed-Om sqrt X(2.33) T1 1.93/1.14/0.00, T2 1.97/1.24/0.00 each within 0.05.
- V2 = KA2 flat injection (Om 0.30, own-X=1 model, new-pair errors): T1 Om 0.30 D_band < 0.05, best sqrt X(2.33) within 0.03 of 1.
- V3 = KA3: profile minimum within 0.1 of the free fit in every cell (by construction of reading 2 this checks the free fit
  is not ABOVE the profile by more than 0.1; reported as the gap).
**New pair (replaces old):** D_M/r_d 39.32 +- 0.33, D_H/r_d 8.600 +- 0.066, r +0.225 (Eq. 26), PROVISIONAL, read 2026-11-12
from https://arxiv.org/html/2607.27410v3 (abstract https://arxiv.org/abs/2607.27410 matches the two values).
**Mutation:** the frozen one: new D_H/r_d -> 8.270 (-5 sigma), D_M unchanged; must bite: T2 Om 0.30 best sqrt X(2.33) up by
>= 0.2 and D_band up by >= 4.
**Determinism:** fixed starts, Nelder-Mead then Powell, OMP/OPENBLAS/MKL threads = 1, `nice -n 19`.
**Hand estimate (contaminated by the disclosure above):** new D_H 0.4 % lower and D_M 0.9 % higher than old -> X5 up a little from
CFG681's 1.24^2: sqrt X(2.33) ~1.3 at T2 Om 0.30, D_band ~2, D_rival >> 4 -> FLAT HOLDS; Om 0.25 (sqrt X ~2) likely differs.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
